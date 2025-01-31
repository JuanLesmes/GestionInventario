# inventory_view.py
import tkinter as tk
from tkinter import ttk

class AdminView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Ajustes principales de la ventana (aprox. 800x600)
        self.config(width=800, height=600)
        self.pack_propagate(False)  # Para respetar el tamaño fijo si lo deseas
        self.pack(fill="both", expand=True)
        
        # Crear estilos específicos para la tabla (opcional)
        self.create_table_styles()
        
        # Crear la interfaz
        self.create_widgets()

    def create_widgets(self):
        """
        Crea toda la interfaz, dividiéndola en:
        1. Cabecera (Header)
        2. Barra lateral izquierda (Sidebar)
        3. Contenido principal (Tabla)
        """
        # Colores y fuentes
        self.color_turquesa = "#00BFBF"
        self.color_naranja  = "#FFA500"
        self.color_gris     = "#F0F0F0"
        self.color_blanco   = "#FFFFFF"
        self.color_azul     = "#0000FF"
        self.color_verde    = "#28A745"
        self.color_amarillo = "#FFD700"
        self.color_borde    = "#D3D3D3"
        
        # Fuentes (aprox. “Sans-serif”)
        self.font_header  = ("Sans-serif", 20, "bold")
        self.font_button  = ("Sans-serif", 14, "bold")
        self.font_label   = ("Sans-serif", 14, "bold")
        self.font_table   = ("Sans-serif", 14)
        
        # ----------------------------------------------------------------
        # 1. Cabecera
        # ----------------------------------------------------------------
        header_height = 60
        header_frame = tk.Frame(self, bg=self.color_turquesa, height=header_height)
        header_frame.pack(side="top", fill="x")
        header_frame.pack_propagate(False)  # Forzar altura fija
        
        # Título
        title_label = tk.Label(
            header_frame,
            text="Control de Inventario",
            bg=self.color_turquesa,
            fg="#FFFFFF",
            font=self.font_header
        )
        title_label.pack(side="left", padx=20)
        
        # Botón "Volver al Menú"
        back_button = tk.Button(
            header_frame,
            text="Volver al Menú",
            bg=self.color_naranja,
            fg="#000000",
            font=self.font_button,
            bd=0,
            cursor="hand2",
            command=self.controller.show_login_view  # Ajustar método según tu controlador
        )
        # Ajustar tamaño aproximado (120x40) con 'width' y 'height' depende de la fuente en Tk
        back_button.config(width=12, height=1)
        back_button.pack(side="right", padx=20, pady=10)
        
        # ----------------------------------------------------------------
        # Contenedor principal: sidebar + contenido
        # ----------------------------------------------------------------
        main_frame = tk.Frame(self, bg=self.color_gris)
        main_frame.pack(side="top", fill="both", expand=True)
        
        # 2. Barra lateral izquierda (25% del ancho)
        sidebar_width = int(800 * 0.25)  # Aprox. 25% de 800
        sidebar_frame = tk.Frame(main_frame, bg=self.color_gris, width=sidebar_width)
        sidebar_frame.pack(side="left", fill="y", padx=20, pady=20)
        sidebar_frame.pack_propagate(False)
        
        # Filtros
        # Combobox “Categoría” (valores: “Todas” por defecto)
        category_label = tk.Label(sidebar_frame, text="Categoría:", bg=self.color_gris, font=self.font_label)
        category_label.pack(anchor="w", pady=5)
        
        self.category_combobox = ttk.Combobox(
            sidebar_frame,
            values=["Todas"],
            state="readonly"
        )
        self.category_combobox.current(0)
        self.category_combobox.config(width=15)
        self.category_combobox.pack(pady=5)
        
        # Botón Filtrar por Categoría
        self.filter_button = tk.Button(
            sidebar_frame,
            text="Filtrar por Categoría",
            bg=self.color_azul,
            fg=self.color_blanco,
            font=self.font_button,
            bd=0,
            cursor="hand2",
            command=self.on_filter_click
        )
        # Aprox. 150x40 => width=15, height=2
        self.filter_button.config(width=18, height=2)
        self.filter_button.pack(pady=5)
        
        # Campo de búsqueda
        self.search_entry = tk.Entry(sidebar_frame, width=20, font=("Sans-serif", 12))
        self.search_entry.pack(pady=5)
        
        # Botones de Gestión
        #  a) Agregar Categoría
        self.add_category_button = tk.Button(
            sidebar_frame,
            text="Agregar Categoría",
            bg=self.color_verde,
            fg="#FFFFFF",
            font=self.font_button,
            bd=0,
            cursor="hand2",
            command=self.on_add_category
        )
        self.add_category_button.config(width=18, height=2)
        self.add_category_button.pack(pady=5)
        
        #  b) Gestionar Producto
        self.manage_product_button = tk.Button(
            sidebar_frame,
            text="Gestionar Producto",
            bg=self.color_amarillo,
            fg="#000000",
            font=self.font_button,
            bd=0,
            cursor="hand2",
            command=self.on_manage_product
        )
        self.manage_product_button.config(width=18, height=2)
        self.manage_product_button.pack(pady=5)
        
        # Valorización Inventario
        valuation_label_title = tk.Label(sidebar_frame, text="Valorización Inventario", bg=self.color_gris, font=self.font_label)
        valuation_label_title.pack(pady=(20, 0))
        
        self.valuation_amount_label = tk.Label(sidebar_frame, text="$0", bg=self.color_gris, font=("Sans-serif", 16, "bold"))
        self.valuation_amount_label.pack(pady=5)
        
        # 3. Cuerpo Principal (Tabla) => ~75% del ancho
        content_frame = tk.Frame(main_frame, bg=self.color_blanco)
        content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # Título de la tabla (alineado a la derecha según tu descripción,
        # pero en tu screenshot parece a la izquierda. Ajusta anchor si lo deseas)
        products_label = tk.Label(
            content_frame,
            text="Productos en Inventario",
            bg=self.color_blanco,
            fg="#000000",
            font=("Sans-serif", 16, "bold"),
            anchor="e"  # "e" para derecha, "w" para izquierda
        )
        products_label.pack(fill="x", pady=5)
        
        # Frame para la tabla y el scrollbar
        table_frame = tk.Frame(content_frame, bg=self.color_blanco, bd=1, relief="solid")
        table_frame.pack(fill="both", expand=True)
        
        # Treeview (tabla)
        columns = ("code", "name", "stock", "cost", "price", "category", "description")
        self.inventory_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Inventory.Treeview"
        )
        # Definir encabezados
        self.inventory_tree.heading("code", text="Código Producto")
        self.inventory_tree.heading("name", text="Nombre Producto")
        self.inventory_tree.heading("stock", text="Stock")
        self.inventory_tree.heading("cost", text="Costo")
        self.inventory_tree.heading("price", text="Precio")
        self.inventory_tree.heading("category", text="Categoría")
        self.inventory_tree.heading("description", text="Descripción")
        
        # Ajuste de columnas
        self.inventory_tree.column("code", width=100, anchor="w")
        self.inventory_tree.column("name", width=150, anchor="w")
        self.inventory_tree.column("stock", width=60, anchor="center")
        self.inventory_tree.column("cost", width=80, anchor="e")
        self.inventory_tree.column("price", width=80, anchor="e")
        self.inventory_tree.column("category", width=120, anchor="w")
        self.inventory_tree.column("description", width=200, anchor="w")
        
        self.inventory_tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar vertical
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.inventory_tree.yview)
        self.inventory_tree.configure(yscroll=scrollbar_y.set)
        scrollbar_y.pack(side="right", fill="y")
        
        # Mensaje por defecto si la tabla está vacía
        self.inventory_tree.insert("", "end", values=("", "Tabla sin contenido", "", "", "", "", ""))
    
    def create_table_styles(self):
        """
        Crea estilos personalizados para la tabla (encabezados con fondo turquesa, texto blanco, etc.).
        """
        style = ttk.Style()
        style.theme_use("clam")
        
        # Encabezados de la tabla (columns heading)
        style.configure(
            "Inventory.Treeview.Heading",
            background="#00BFBF",
            foreground="#FFFFFF",
            font=("Sans-serif", 14, "bold")
        )
        # Filas de la tabla
        style.configure(
            "Inventory.Treeview",
            font=("Sans-serif", 12),
            rowheight=25,
            bordercolor="#D3D3D3",
            borderwidth=1
        )
        style.map("Inventory.Treeview", background=[("selected", "#00BFBF")])  # color al seleccionar una fila
    
    # --------------------------------------------------------------------------
    # Métodos de ejemplo para enlazar con tu controlador o lógica
    # --------------------------------------------------------------------------
    def on_filter_click(self):
        """Evento para el botón 'Filtrar por Categoría'."""
        print("Filtrando por:", self.category_combobox.get())
        # Llama a un método del controlador para filtrar los productos...
    
    def on_add_category(self):
        """Evento para el botón 'Agregar Categoría'."""
        print("Agregando categoría... (llamar controlador)")
    
    def on_manage_product(self):
        """Evento para el botón 'Gestionar Producto'."""
        print("Gestionar producto... (llamar controlador)")
