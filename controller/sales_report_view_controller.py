import tkinter as tk
from tkinter import messagebox
import datetime

class SalesReportViewController:
    def __init__(self, parent, main_controller, db):
        self.parent = parent
        self.main_controller = main_controller
        self.db = db
        from view.sales_report_view import SalesReportView
        self.view = SalesReportView(self.parent, self)
        self.initialize()

    def initialize(self):
        self.view.load_table([])  # Empty at start
        self.view.set_totals(0.0, 0.0, 0.0, 0.0)

    def event_back(self):
        self.main_controller.show_stonks_view()

    def event_search(self):
        start_date = self.view.get_start_date()
        end_date = self.view.get_end_date()
        if start_date is None or end_date is None:
            messagebox.showerror("No Dates", "Please select start and end dates.")
            return
        receipts = self.db.get_receipts_in_range(start_date, end_date)
        sold_products = self.aggregate_sold_products(receipts)
        self.view.load_table(sold_products)
        rec_total, cash, card, transfer = self.calculate_totals(receipts)
        self.view.set_totals(rec_total, cash, card, transfer)

    def aggregate_sold_products(self, receipts):
        aggregated = {}
        for r in receipts:
            for sp in r.sold_products:
                if sp.get_code() in aggregated:
                    aggregated[sp.get_code()].quantity += sp.quantity
                    aggregated[sp.get_code()].calculate_total_partial()
                else:
                    # Clone sp
                    from model.sold_product import SoldProduct
                    new_sp = SoldProduct(0, sp.product, sp.quantity)
                    aggregated[sp.get_code()] = new_sp
        return list(aggregated.values())

    def calculate_totals(self, receipts):
        total = 0.0
        cash = 0.0
        card = 0.0
        transfer = 0.0
        for r in receipts:
            total += r.total_sale
            if r.payment_method == "Cash":
                cash += r.total_sale
            elif r.payment_method == "Card":
                card += r.total_sale
            elif r.payment_method == "Transfer":
                transfer += r.total_sale
        return total, cash, card, transfer
