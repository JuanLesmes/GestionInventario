import tkinter as tk
from tkinter import simpledialog, messagebox
from model.product import Product

class ProductManagementViewController:
    def __init__(self, parent, main_controller, db):
        self.parent = parent
        self.main_controller = main_controller
        self.db = db
        from view.product_management_view import ProductManagementView
        self.view = ProductManagementView(self.parent, self)
        self.initialize()

    def initialize(self):
        self.view.load_categories(self.db.get_categories())

    def event_back(self):
        self.main_controller.show_admin_view()

    def event_search_by_code(self):
        code = self.view.get_product_code().strip()
        if code == "":
            messagebox.showerror("No Code", "Please enter a product code.")
            return
        product = self.db.get_product(code)
        if product is None:
            messagebox.showwarning("Not Found", "No product found with that code.")
        else:
            self.view.show_product(product)

    def event_add_product(self):
        if self.view.check_fields():
            code = self.view.get_product_code().strip()
            existing = self.db.get_product(code)
            if existing is not None:
                messagebox.showwarning("Existing Product", "This product already exists.")
                return
            name = self.view.get_product_name().strip()
            cost = float(self.view.get_product_cost())
            price = float(self.view.get_product_price())
            stock = int(self.view.get_product_stock())
            category = self.view.get_product_category()
            description = self.view.get_product_description().strip()

            product = Product(code, name, cost, price, stock, category, description)
            self.db.add_product(product)
            messagebox.showinfo("Success", "Product added successfully.")
            self.view.clear_fields()

    def event_modify_product(self):
        if self.view.check_fields():
            code = self.view.get_product_code().strip()
            product = self.db.get_product(code)
            if product is None:
                messagebox.showwarning("Not Found", "This product does not exist.")
                return
            # Compare and update fields
            name = self.view.get_product_name().strip()
            cost = float(self.view.get_product_cost())
            price = float(self.view.get_product_price())
            stock = int(self.view.get_product_stock())
            category = self.view.get_product_category()
            description = self.view.get_product_description().strip()

            changes = []
            if product.name != name:
                self.db.update_product_name(code, name)
                changes.append("Name")
            if product.cost != cost:
                self.db.update_cost(code, cost)
                changes.append("Cost")
            if product.price != price:
                self.db.update_price(code, price)
                changes.append("Price")
            if product.category != category:
                self.db.update_category(code, category)
                changes.append("Category")
            if product.description != description:
                self.db.update_description(code, description)
                changes.append("Description")

            if changes:
                messagebox.showinfo("Modified", f"The following attributes were modified: {', '.join(changes)}")
                self.view.clear_fields()
            else:
                messagebox.showinfo("No Changes", "No changes made.")

    def event_delete_product(self):
        code = self.view.get_product_code().strip()
        if code == "":
            messagebox.showerror("No Code", "Please enter a product code.")
            return
        product = self.db.get_product(code)
        if product is None:
            messagebox.showwarning("Not Found", "This product does not exist.")
            return
        resp = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this product?")
        if resp:
            # Delete by setting stock to 0 or similar logic
            self.db.update_stock(code, -(product.stock+1))
            messagebox.showinfo("Deleted", "Product deleted (stock set to 0, not shown in inventory).")
            self.view.clear_fields()

    def event_add_stock(self):
        code = self.view.get_product_code().strip()
        if code == "":
            messagebox.showerror("No Code", "Please enter a product code.")
            return
        product = self.db.get_product(code)
        if product is None:
            messagebox.showwarning("Not Found", "This product does not exist.")
            return
        quantity_str = simpledialog.askstring("Add Stock", "Enter the quantity to add:")
        if quantity_str is not None and quantity_str.strip() != "":
            try:
                quantity = int(quantity_str)
                if quantity > 0:
                    self.db.update_stock(code, quantity)
                    messagebox.showinfo("Success", "Stock updated successfully.")
                    # Refresh product info
                    updated_product = self.db.get_product(code)
                    self.view.show_product(updated_product)
                else:
                    messagebox.showerror("Invalid Quantity", "Quantity must be greater than zero.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid integer quantity.")
