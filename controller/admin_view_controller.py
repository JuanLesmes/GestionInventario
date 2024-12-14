from tkinter import messagebox

class AdminViewController:
    def __init__(self, parent, main_controller, db):
        self.parent = parent
        self.main_controller = main_controller
        self.db = db
        from view.admin_view import AdminView
        self.view = AdminView(self.parent, self)
        self.initialize()

    def initialize(self):
        products = self.db.get_products()
        self.view.load_table(products)
        self.view.set_inventory_value(self.calculate_inventory_value(products))
        self.view.set_categories(self.db.get_categories())

    def calculate_inventory_value(self, products):
        total = 0.0
        for p in products:
            total += p.price * p.stock
        return total

    def event_back(self):
        self.main_controller.show_stonks_view()

    def event_filter(self):
        category = self.view.get_selected_category()
        if category == "" or category == "All":
            products = self.db.get_products()
        else:
            products = self.db.get_products_by_category(category)
        self.view.load_table(products)

    def event_manage_products(self):
        self.main_controller.show_product_management_view()

    def event_add_category(self):
        new_cat = self.view.get_new_category()
        if new_cat == "":
            messagebox.showerror("Invalid Category", "No text entered! Please enter a category name.")
        else:
            categories = self.db.get_categories()
            if new_cat in categories:
                messagebox.showwarning("Category Exists", f"This category already exists: {new_cat}")
            else:
                self.db.add_category(new_cat)
                messagebox.showinfo("Category Added", f"Category {new_cat} added successfully.")
                self.view.clear_new_category()
                self.view.set_categories(self.db.get_categories())
