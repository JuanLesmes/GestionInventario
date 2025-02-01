import sqlite3
from model.product import Product
from model.receipt import Receipt
from model.sold_product import SoldProduct
import datetime
import os
import sys

class DBConnection:
    def __init__(self, db_path="data/local.db"):
        # Si el programa está empaquetado (frozen), utiliza sys._MEIPASS para obtener la carpeta temporal
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        db_full_path = os.path.join(base_path, db_path)
        self.conn = sqlite3.connect(db_full_path)
        self.conn.execute("PRAGMA foreign_keys = 1;")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Create tables similar to original Java code
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            idCategory INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT
        );
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            code TEXT PRIMARY KEY,
            name TEXT,
            cost REAL,
            price REAL,
            stock INTEGER,
            category INTEGER,
            description TEXT,
            FOREIGN KEY(category) REFERENCES categories(idCategory)
        );
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS receipts (
            idReceipt INTEGER PRIMARY KEY AUTOINCREMENT,
            total REAL,
            date TEXT,
            time TEXT,
            payment_method TEXT
        );
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS sold_products (
            idSale INTEGER PRIMARY KEY AUTOINCREMENT,
            idReceipt INTEGER,
            codeP TEXT,
            quantity INTEGER,
            FOREIGN KEY(idReceipt) REFERENCES receipts(idReceipt),
            FOREIGN KEY(codeP) REFERENCES products(code)
        );
        """)
        self.conn.commit()

    def get_categories(self):
        cats = []
        self.cursor.execute("SELECT category_name FROM categories")
        rows = self.cursor.fetchall()
        for r in rows:
            cats.append(r[0])
        return cats

    def add_category(self, category_name):
        self.cursor.execute("INSERT INTO categories (category_name) VALUES (?)", (category_name,))
        self.conn.commit()

    def get_category_id(self, cat_name):
        self.cursor.execute("SELECT idCategory FROM categories WHERE category_name=?", (cat_name,))
        row = self.cursor.fetchone()
        if row:
            return row[0]
        return None

    def delete_category(self, category_name):
        """
        Elimina la categoría de la tabla 'categories' cuyo nombre sea category_name.
        Devuelve True si se eliminó correctamente o False en caso de error.
        """
        try:
            self.cursor.execute("DELETE FROM categories WHERE category_name = ?", (category_name,))
            self.conn.commit()
            return True
        except Exception as e:
            print("Error al eliminar categoría:", e)
            return False

    def get_products(self):
        products = []
        self.cursor.execute("""
            SELECT p.code, p.name, p.cost, p.price, p.stock, c.category_name, p.description
            FROM products p
            JOIN categories c ON p.category=c.idCategory
            WHERE p.stock > 0
        """)
        rows = self.cursor.fetchall()
        for r in rows:
            products.append(Product(r[0], r[1], r[2], r[3], r[4], r[5], r[6]))
        return products

    def get_products_by_category(self, cat):
        products = []
        self.cursor.execute("""
            SELECT p.code, p.name, p.cost, p.price, p.stock, c.category_name, p.description
            FROM products p
            JOIN categories c ON p.category=c.idCategory
            WHERE c.category_name=? AND p.stock > 0
        """, (cat,))
        rows = self.cursor.fetchall()
        for r in rows:
            products.append(Product(r[0], r[1], r[2], r[3], r[4], r[5], r[6]))
        return products

    def get_product(self, code):
        self.cursor.execute("""
            SELECT p.code, p.name, p.cost, p.price, p.stock, c.category_name, p.description
            FROM products p
            JOIN categories c ON p.category=c.idCategory
            WHERE p.code=?
        """, (code,))
        r = self.cursor.fetchone()
        if r:
            return Product(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
        return None

    def add_product(self, product):
        cat_id = self.get_category_id(product.category)
        if cat_id is None:
            # If category doesn't exist, create it automatically
            self.add_category(product.category)
            cat_id = self.get_category_id(product.category)
        self.cursor.execute("""
            INSERT INTO products (code, name, cost, price, stock, category, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            product.code,
            product.name,
            product.cost,
            product.price,
            product.stock,
            cat_id,
            product.description
        ))
        self.conn.commit()

    def update_product_name(self, code, name):
        self.cursor.execute("UPDATE products SET name=? WHERE code=?", (name, code))
        self.conn.commit()

    def update_cost(self, code, cost):
        self.cursor.execute("UPDATE products SET cost=? WHERE code=?", (cost, code))
        self.conn.commit()

    def update_price(self, code, price):
        self.cursor.execute("UPDATE products SET price=? WHERE code=?", (price, code))
        self.conn.commit()

    def update_description(self, code, description):
        self.cursor.execute("UPDATE products SET description=? WHERE code=?", (description, code))
        self.conn.commit()

    def update_category(self, code, category_name):
        cat_id = self.get_category_id(category_name)
        if cat_id is None:
            self.add_category(category_name)
            cat_id = self.get_category_id(category_name)
        self.cursor.execute("UPDATE products SET category=? WHERE code=?", (cat_id, code))
        self.conn.commit()

    def update_stock(self, code, quantity):
        self.cursor.execute("SELECT stock FROM products WHERE code=?", (code,))
        row = self.cursor.fetchone()
        if row:
            new_stock = row[0] + quantity
            self.cursor.execute("UPDATE products SET stock=? WHERE code=?", (new_stock, code))
            self.conn.commit()

    def add_receipt(self, receipt):
        self.cursor.execute("""
            INSERT INTO receipts (total, date, time, payment_method)
            VALUES (?, ?, ?, ?)
        """, (
            receipt.total_sale,
            receipt.date.isoformat(),
            receipt.time.strftime("%H:%M:%S"),
            receipt.payment_method
        ))
        self.conn.commit()
        receipt_id = self.cursor.lastrowid

        # Insert sold products
        for sp in receipt.sold_products:
            self.cursor.execute("""
                INSERT INTO sold_products (idReceipt, codeP, quantity) VALUES (?, ?, ?)
            """, (receipt_id, sp.product.code, sp.quantity))
            # Update stock
            self.update_stock(sp.product.code, -sp.quantity)
        self.conn.commit()

        # Actualiza el ID del recibo
        receipt.id = receipt_id

    def get_receipts_in_range(self, start_date, end_date):
        start_str = start_date.isoformat()
        end_str = end_date.isoformat()
        self.cursor.execute("""
            SELECT idReceipt, total, date, time, payment_method
            FROM receipts
            WHERE date BETWEEN ? AND ?
        """, (start_str, end_str))
        rows = self.cursor.fetchall()
        receipts = []
        for r in rows:
            rec = Receipt(
                id=r[0],
                total_sale=r[1],
                date=datetime.date.fromisoformat(r[2]),
                time=datetime.datetime.strptime(r[3], "%H:%M:%S").time(),
                payment_method=r[4]
            )
            rec.sold_products = self.get_sold_products_for_receipt(rec.id)
            receipts.append(rec)
        return receipts

    def get_sold_products_for_receipt(self, receipt_id):
        self.cursor.execute("SELECT codeP, quantity FROM sold_products WHERE idReceipt=?", (receipt_id,))
        rows = self.cursor.fetchall()
        sps = []
        for r in rows:
            p = self.get_product(r[0])
            if p:
                sp = SoldProduct(receipt_id, p, r[1])
                sps.append(sp)
        return sps
    
    def delete_product(self, code):
        """
        Elimina el producto de la tabla 'products' por su código.
        Asegúrate de tener PRAGMA foreign_keys=1 y ON DELETE CASCADE 
        si hay referencias a este producto en otras tablas.
        """
        self.cursor.execute("DELETE FROM products WHERE code = ?", (code,))
        self.conn.commit()
