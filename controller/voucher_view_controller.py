import tkinter as tk

class VoucherViewController:
    def __init__(self, parent, main_controller, db):
        self.parent = parent
        self.main_controller = main_controller
        self.db = db
        from view.voucher_view import VoucherView
        self.view = VoucherView(self.parent, self)
        self.receipt = None
        self.change_due = 0.0

    def load_receipt(self, receipt, change_due):
        self.receipt = receipt
        self.change_due = change_due
        self.view.show_receipt(receipt, change_due)

    def event_back_to_sales(self):
        self.main_controller.show_sales_view()
