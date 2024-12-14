# view/sales_report_view.py
import tkinter as tk

class SalesReportView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
        self.pack(fill="both", expand=True)

    def create_widgets(self):
        title_label = tk.Label(self, text="Sales Report View", font=("Arial", 24, "bold"))
        title_label.pack(pady=20)

        back_button = tk.Button(self, text="Back to Login View", command=self.controller.show_login_view)
        back_button.pack(pady=10)
