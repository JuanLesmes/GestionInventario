import tkinter as tk
from tkinter import simpledialog, messagebox
from model.sold_product import SoldProduct
from model.receipt import Receipt
import datetime

class SalesViewController:
    def __init__(self, parent, main_controller, db):
        self.parent = parent
        self.main_controller = main_controller
        self.db = db
        from view.sales_view import SalesView
        self.view = SalesView(self.parent, self)
        self.sold_products = []
        self.initialize()

    def initialize(self):
        self.sold_products = []
        self.view.load_table(self.sold_products)
        self.view.set_total("0.0")

    def event_back(self):
        self.main_controller.show_stonks_view()

    def event_add_product(self):
        code = simpledialog.askstring("Add Product", "Enter Product Code:")
        if code is None or code.strip() == "":
            return
        product = self.db.get_product(code.strip())
        if product is None or product.stock <= 0:
            messagebox.showwarning("Error", "Product not found or no stock.")
            return
        qty_str = simpledialog.askstring("Quantity", "Enter quantity:")
        if qty_str is None or qty_str.strip() == "":
            return
        try:
            qty = int(qty_str)
            if qty <= 0 or qty > product.stock:
                messagebox.showwarning("Error", f"Invalid quantity. Available stock: {product.stock}")
                return
            # Check if product already in sold_products
            for sp in self.sold_products:
                if sp.get_code() == product.code:
                    new_qty = sp.quantity + qty
                    if new_qty > product.stock:
                        messagebox.showwarning("Error", f"Not enough stock. Available: {product.stock}")
                        return
                    sp.quantity = new_qty
                    sp.calculate_total_partial()
                    break
            else:
                sp = SoldProduct(0, product, qty)
                self.sold_products.append(sp)
            self.refresh_sales_table()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer.")

    def event_remove_product(self):
        code = simpledialog.askstring("Remove Product", "Enter product code to remove:")
        if code is None or code.strip() == "":
            return
        removed = False
        for i, sp in enumerate(self.sold_products):
            if sp.get_code() == code.strip():
                self.sold_products.pop(i)
                removed = True
                break
        if removed:
            self.refresh_sales_table()
        else:
            messagebox.showwarning("Error", "Product not found in the sale list.")

    def refresh_sales_table(self):
        self.view.load_table(self.sold_products)
        self.view.set_total(self.calculate_total())

    def calculate_total(self):
        total = 0.0
        for sp in self.sold_products:
            total += sp.total_partial
        return f"{total:.2f}"

    def event_cash_payment(self):
        total_sale = float(self.calculate_total())
        if total_sale == 0.0:
            messagebox.showerror("Error", "No products in the sale.")
            return
        val_str = self.view.get_received_amount().strip()
        if val_str == "":
            messagebox.showerror("Error", "Please enter the received amount.")
            return
        try:
            received = float(val_str)
            if received < total_sale:
                messagebox.showerror("Error", "Received amount is not enough.")
                return
            change_due = received - total_sale
            self.generate_receipt("Cash", total_sale, change_due)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount received.")

    def event_card_payment(self):
        total_sale = float(self.calculate_total())
        if total_sale == 0.0:
            messagebox.showerror("Error", "No products in the sale.")
            return
        self.generate_receipt("Card", total_sale, 0.0)

    def event_transfer_payment(self):
        total_sale = float(self.calculate_total())
        if total_sale == 0.0:
            messagebox.showerror("Error", "No products in the sale.")
            return
        self.generate_receipt("Transfer", total_sale, 0.0)

    def generate_receipt(self, payment_method, total_sale, change_due):
        # Create receipt
        now = datetime.datetime.now()
        receipt = Receipt(date=now.date(), time=now.time(), payment_method=payment_method)
        receipt.sold_products = self.sold_products
        receipt.total_sale = total_sale
        self.db.add_receipt(receipt)
        # Show voucher
        self.main_controller.show_voucher_view(receipt, change_due)
