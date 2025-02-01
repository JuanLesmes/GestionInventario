# controller/product_management_view_controller.py

import tkinter as tk
from tkinter import messagebox
from model.product import Product

class ProductManagementViewController:
    def __init__(self, parent, main_controller, db):
        """
        parent: un Frame contenedor (ej: self.frame_product_mgmt en main_controller)
        main_controller: para volver a otras vistas, etc.
        db: instancia de DBConnection
        """
        self.parent = parent
        self.main_controller = main_controller
        self.db = db

        from view.product_management_view import ProductManagementView
        self.view = ProductManagementView(self.parent, self)

        # Cargar categorías en el combo
        cats = self.db.get_categories()  # Devuelve lista de nombres
        self.view.set_categories(cats)

    # --------------------------
    # Métodos (eventos) de la vista
    # --------------------------
    def event_go_back_to_inventory(self):
        """
        Botón "Volver a Gestión de Inventario".
        Navega a la vista Admin/Inventario.
        """
        self.main_controller.show_admin_view()

    def event_search_scan(self):
        """
        Botón "Buscar Por Scan".
        Podrías implementar una lectura de código de barras, etc.
        """
        code = self.view.get_code()
        if not code:
            messagebox.showwarning("Alerta", "Ingrese un código para escanear/buscar.")
            return
        
        product = self.db.get_product(code)
        if product:
            self.fill_form_with_product(product)
        else:
            messagebox.showinfo("Info", f"No se encontró el producto con código {code}.")

    def event_search_manual(self):
        """
        Botón "Buscar Manual".
        Similar a 'Buscar Por Scan', pero quizás pida datos extra 
        o muestre un popup. Aquí lo simplificamos.
        """
        code = self.view.get_code()
        if not code:
            messagebox.showwarning("Alerta", "Ingrese un código para buscar manualmente.")
            return

        product = self.db.get_product(code)
        if product:
            self.fill_form_with_product(product)
        else:
            messagebox.showinfo("Info", f"No se encontró el producto con código {code}.")

    def event_add_stock(self):
        """
        Botón "Agregar Stock".
        Suma el stock ingresado al stock actual del producto (buscando por código).
        """
        code = self.view.get_code()
        if not code:
            messagebox.showwarning("Alerta", "Ingrese un código de producto para agregar stock.")
            return
        
        product = self.db.get_product(code)
        if not product:
            messagebox.showinfo("Info", f"No se encontró el producto con código {code}.")
            return

        # Tomamos la cantidad en "Stock" del formulario como la cantidad a sumar
        stock_str = self.view.get_stock()
        try:
            add_qty = int(stock_str)
        except ValueError:
            messagebox.showerror("Error", "La cantidad de stock a agregar debe ser un número entero.")
            return
        
        if add_qty <= 0:
            messagebox.showerror("Error", "La cantidad a agregar debe ser mayor a 0.")
            return

        # Actualizamos en BD
        self.db.update_stock(code, add_qty)
        messagebox.showinfo("Stock Actualizado", f"Se agregaron {add_qty} unidades al producto {code}.")

        # Volvemos a mostrar el nuevo stock en el formulario
        updated_product = self.db.get_product(code)
        if updated_product:
            self.fill_form_with_product(updated_product)

    def event_add_product(self):
        """
        Botón "Agregar Producto".
        Toma los campos y crea un nuevo registro en la BD.
        """
        code = self.view.get_code()
        name = self.view.get_name()
        stock_str = self.view.get_stock()
        cost_str = self.view.get_cost()
        price_str = self.view.get_price()
        category = self.view.get_category()
        desc = self.view.get_description()

        # Validar campos mínimos
        if not code or not name:
            messagebox.showerror("Error", "Código y Nombre son obligatorios.")
            return

        try:
            stock = int(stock_str) if stock_str else 0
            cost = float(cost_str) if cost_str else 0.0
            price = float(price_str) if price_str else 0.0
        except ValueError:
            messagebox.showerror("Error", "Stock, Costo y Precio deben ser numéricos.")
            return

        # Ver si ya existe el producto
        existing = self.db.get_product(code)
        if existing:
            messagebox.showwarning("Error", f"Ya existe un producto con código {code}.")
            return

        # Crear Product y guardar en BD
        new_prod = Product(
            code=code,
            name=name,
            cost=cost,
            price=price,
            stock=stock,
            category=category,
            description=desc
        )
        self.db.add_product(new_prod)

        messagebox.showinfo("Éxito", f"Producto '{name}' agregado correctamente.")
        self.view.clear_fields()

    def event_modify_product(self):
        """
        Botón "Modificar Producto".
        Actualiza los datos en BD del producto con el código actual.
        """
        code = self.view.get_code()
        if not code:
            messagebox.showerror("Error", "Ingrese el código del producto a modificar.")
            return

        # Verificar si existe
        product = self.db.get_product(code)
        if not product:
            messagebox.showinfo("Info", f"No se encontró el producto con código {code}.")
            return

        # Leer campos
        name = self.view.get_name()
        stock_str = self.view.get_stock()
        cost_str = self.view.get_cost()
        price_str = self.view.get_price()
        category = self.view.get_category()
        desc = self.view.get_description()

        # Convertir a números
        try:
            stock = int(stock_str) if stock_str else 0
            cost = float(cost_str) if cost_str else 0.0
            price = float(price_str) if price_str else 0.0
        except ValueError:
            messagebox.showerror("Error", "Stock, Costo y Precio deben ser numéricos.")
            return

        # Actualizar en BD (podemos usar los métodos update_cost, update_price, etc.)
        # O ver si tienes un update general. Ejemplo:
        self.db.update_product_name(code, name)
        self.db.update_stock(code, stock - product.stock)  # stock actual - stock original
        self.db.update_cost(code, cost)
        self.db.update_price(code, price)
        self.db.update_description(code, desc)
        self.db.update_category(code, category)

        messagebox.showinfo("Éxito", f"Producto '{code}' modificado correctamente.")

    def event_delete_product(self):
        code = self.view.get_code()
        if not code:
            messagebox.showerror("Error", "Ingrese el código del producto a eliminar.")
            return

        product = self.db.get_product(code)
        if not product:
            messagebox.showinfo("Info", f"No se encontró el producto con código {code}.")
            return

        confirm = messagebox.askyesno(
            "Confirmar",
            f"¿Está seguro de eliminar el producto '{product.name}' (código {code})?"
        )
        if confirm:
            self.db.delete_product(code)  # <-- Ya implementado en DBConnection
            messagebox.showinfo("Borrado", f"Producto {code} eliminado.")
            self.view.clear_fields()

    
    # ----------------------------------------------
    # Métodos internos
    # ----------------------------------------------
    def fill_form_with_product(self, product):
        """
        Rellena los campos del formulario con la info del producto.
        """
        self.view.set_code(product.code)
        self.view.set_name(product.name)
        self.view.set_stock(str(product.stock))
        self.view.set_cost(str(product.cost))
        self.view.set_price(str(product.price))
        self.view.set_description(product.description)
        
        # Fijar la categoría en el combo si existe
        cats = self.db.get_categories()
        self.view.set_categories(cats)
        if product.category in cats:
            idx = cats.index(product.category)
            self.view.cmb_category.current(idx)
