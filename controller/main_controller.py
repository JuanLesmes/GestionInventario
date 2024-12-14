import tkinter as tk
from model.db_connection import DBConnection

class MainController:
    def __init__(self, root):
        self.root = root
        self.root.title("InventoryManagement")
        self.db = DBConnection()

        from controller.stonks_view_controller import StonksViewController
        self.frame_stonks = tk.Frame(self.root)
        self.stonks_controller = StonksViewController(self.frame_stonks, self, self.db)

        from controller.admin_view_controller import AdminViewController
        self.frame_admin = tk.Frame(self.root)
        self.admin_controller = AdminViewController(self.frame_admin, self, self.db)

        from controller.product_management_view_controller import ProductManagementViewController
        self.frame_product_mgmt = tk.Frame(self.root)
        self.product_mgmt_controller = ProductManagementViewController(self.frame_product_mgmt, self, self.db)

        from controller.sales_view_controller import SalesViewController
        self.frame_sales = tk.Frame(self.root)
        self.sales_controller = SalesViewController(self.frame_sales, self, self.db)

        from controller.sales_report_view_controller import SalesReportViewController
        self.frame_sales_report = tk.Frame(self.root)
        self.sales_report_controller = SalesReportViewController(self.frame_sales_report, self, self.db)

        from controller.voucher_view_controller import VoucherViewController
        self.frame_voucher = tk.Frame(self.root)
        self.voucher_controller = VoucherViewController(self.frame_voucher, self, self.db)

        self.show_stonks_view()

    def show_stonks_view(self):
        self.hide_all_frames()
        self.frame_stonks.pack(fill="both", expand=True)

    def show_admin_view(self):
        self.hide_all_frames()
        self.frame_admin.pack(fill="both", expand=True)

    def show_product_management_view(self):
        self.hide_all_frames()
        self.frame_product_mgmt.pack(fill="both", expand=True)

    def show_sales_view(self):
        self.hide_all_frames()
        self.frame_sales.pack(fill="both", expand=True)

    def show_sales_report_view(self):
        self.hide_all_frames()
        self.frame_sales_report.pack(fill="both", expand=True)

    def show_voucher_view(self, receipt, change_due):
        # Show voucher view with given data
        self.voucher_controller.load_receipt(receipt, change_due)
        self.hide_all_frames()
        self.frame_voucher.pack(fill="both", expand=True)

    def hide_all_frames(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()
