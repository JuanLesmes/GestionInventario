# controller/main_controller.py
import tkinter as tk

class MainController:
    def __init__(self, root):
        self.root = root
        self.root.title("InventoryManagement")

        from view.login_view import LoginView
        from view.admin_view import AdminView
        from view.product_management_view import ProductManagementView
        from view.sales_view import SalesView
        from view.sales_report_view import SalesReportView
        from view.voucher_view import VoucherView

        # LoginView
        self.frame_login = tk.Frame(self.root)
        self.login_view = LoginView(self.frame_login, self)

        # AdminView
        self.frame_admin = tk.Frame(self.root)
        self.admin_view = AdminView(self.frame_admin, self)

        # ProductManagementView
        self.frame_product_mgmt = tk.Frame(self.root)
        self.product_mgmt_view = ProductManagementView(self.frame_product_mgmt, self)

        # SalesView
        self.frame_sales = tk.Frame(self.root)
        self.sales_view = SalesView(self.frame_sales, self)

        # SalesReportView
        self.frame_sales_report = tk.Frame(self.root)
        self.sales_report_view = SalesReportView(self.frame_sales_report, self)

        # VoucherView
        self.frame_voucher = tk.Frame(self.root)
        self.voucher_view = VoucherView(self.frame_voucher, self)

        self.show_login_view()  # Mostramos la vista principal (login)

    def show_login_view(self):
        self.hide_all_frames()
        self.frame_login.pack(fill="both", expand=True)

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

    def show_voucher_view(self):
        self.hide_all_frames()
        self.frame_voucher.pack(fill="both", expand=True)

    def hide_all_frames(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()
