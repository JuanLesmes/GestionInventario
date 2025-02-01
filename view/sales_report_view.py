# sales_report_view.py

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry  # Para mostrar un calendario desplegable

class SalesReportView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Ajustar tamaño base de la ventana
        self.config(width=800, height=600)
        self.pack_propagate(False)
        self.pack(fill="both", expand=True)
        
        # Crear estilos para la tabla (encabezado turquesa, etc.)
        self.create_table_styles()
        
        # Construir la interfaz
        self.create_widgets()
    
    def create_widgets(self):
        # Paleta de colores
        turquesa    = "#00BFBF"
        gris_claro  = "#F0F0F0"
        blanco      = "#FFFFFF"
        azul        = "#0000FF"
        naranja     = "#FFA500"
        gris_borde  = "#D3D3D3"
        
        # Fuentes
        font_header   = ("Sans-serif", 20, "bold")  # para el título "Reporte de Ventas"
        font_label    = ("Sans-serif", 14, "bold")
        font_button   = ("Sans-serif", 14, "bold")
        font_summary  = ("Sans-serif", 14)
        
        # ----------------------------------------------------------------
        # 1. Encabezado (fondo turquesa con título centrado)
        # ----------------------------------------------------------------
        header_height = 60
        header_frame = tk.Frame(self, bg=turquesa, height=header_height)
        header_frame.pack(side="top", fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="Reporte De Ventas",
            bg=turquesa,
            fg="#000000",
            font=font_header
        )
        # Centrado horizontalmente en el frame
        title_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # ----------------------------------------------------------------
        # 2. Cuerpo principal (tabla a la izquierda, filtros+resumen a la derecha)
        # ----------------------------------------------------------------
        body_frame = tk.Frame(self, bg=gris_claro)
        body_frame.pack(side="top", fill="both", expand=True)
        
        # --- Sección Izquierda: Tabla de ventas ---
        table_frame = tk.Frame(body_frame, bg=blanco, bd=1, relief="solid")
        table_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        columns = ("code", "name", "qty", "total")
        self.sales_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="SalesReport.Treeview"
        )
        self.sales_tree.heading("code", text="Código")
        self.sales_tree.heading("name", text="Nombre")
        self.sales_tree.heading("qty", text="Cantidad")
        self.sales_tree.heading("total", text="Total")
        
        self.sales_tree.column("code", width=80)
        self.sales_tree.column("name", width=160)
        self.sales_tree.column("qty", width=80, anchor="center")
        self.sales_tree.column("total", width=80, anchor="e")
        
        self.sales_tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar vertical
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.sales_tree.yview)
        self.sales_tree.configure(yscroll=scrollbar_y.set)
        scrollbar_y.pack(side="right", fill="y")
        
        # Mensaje cuando la tabla está vacía
        self.sales_tree.insert("", "end", values=("", "Tabla sin contenido", "", ""))
        
        # --- Sección Derecha: Filtros de fecha, resumen de montos, botón ---
        right_frame = tk.Frame(body_frame, bg=gris_claro, width=250)
        right_frame.pack(side="right", fill="y", padx=20, pady=20)
        right_frame.pack_propagate(False)
        
        # 2.1 Filtros de fecha (encima de todo)
        filters_frame = tk.Frame(right_frame, bg=gris_claro)
        filters_frame.pack(side="top", fill="x")
        
        # Etiqueta y DateEntry para Fecha Inicio
        start_label = tk.Label(filters_frame, text="Fecha Inicio", bg=gris_claro, fg="#000000", font=font_label)
        start_label.pack(anchor="w", pady=(0,5))
        
        self.start_date = DateEntry(filters_frame, width=15, background="darkblue",
                                    foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd")
        self.start_date.pack(anchor="w", pady=(0,10))
        
        # Etiqueta y DateEntry para Fecha Término
        end_label = tk.Label(filters_frame, text="Fecha Termino", bg=gris_claro, fg="#000000", font=font_label)
        end_label.pack(anchor="w", pady=(0,5))
        
        self.end_date = DateEntry(filters_frame, width=15, background="darkblue",
                                  foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd")
        self.end_date.pack(anchor="w", pady=(0,10))
        
        # Botón "Buscar"
        search_button = tk.Button(
            filters_frame,
            text="Buscar",
            bg=azul,
            fg=blanco,
            font=font_button,
            bd=0,
            cursor="hand2",
            command=self.on_search_click
        )
        search_button.config(width=12, height=1)
        search_button.pack(anchor="w", pady=(10,10))
        
        # 2.2 Resumen de montos
        summary_frame = tk.Frame(right_frame, bg=gris_claro)
        summary_frame.pack(side="top", fill="x", pady=(20, 0))
        
        total_label = tk.Label(summary_frame, text="Total Recaudado", bg=gris_claro, font=("Sans-serif", 16, "bold"))
        total_label.pack(anchor="w", pady=(0,0))
        
        self.total_amount_label = tk.Label(summary_frame, text="$0", bg=gris_claro, font=("Sans-serif", 16, "bold"))
        self.total_amount_label.pack(anchor="w", pady=5)
        
        self.cash_label = tk.Label(summary_frame, text="Efectivo        $0", bg=gris_claro, font=font_summary)
        self.cash_label.pack(anchor="w", pady=5)
        
        self.card_label = tk.Label(summary_frame, text="Tarjeta         $0", bg=gris_claro, font=font_summary)
        self.card_label.pack(anchor="w", pady=5)
        
        self.transfer_label = tk.Label(summary_frame, text="Transferencia  $0", bg=gris_claro, font=font_summary)
        self.transfer_label.pack(anchor="w", pady=5)
        
        # 2.3 Botón "Volver al Menú" al final
        back_button = tk.Button(
            right_frame,
            text="Volver al Menú",
            bg=naranja,
            fg="#000000",
            font=("Sans-serif", 16, "bold"),
            bd=0,
            cursor="hand2",
            command=self.controller.show_login_view  # Ajusta según tu MainController
        )
        back_button.config(width=14, height=2)
        back_button.pack(side="bottom", pady=20)

    def create_table_styles(self):
        """
        Crea un estilo personalizado para la tabla:
        encabezado turquesa, texto blanco, fuente sans-serif 14px negrita.
        """
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure(
            "SalesReport.Treeview.Heading",
            background="#00BFBF",
            foreground="#FFFFFF",
            font=("Sans-serif", 14, "bold")
        )
        style.configure(
            "SalesReport.Treeview",
            font=("Sans-serif", 12),
            rowheight=25,
            bordercolor="#D3D3D3",
            borderwidth=1
        )
        style.map(
            "SalesReport.Treeview",
            background=[("selected", "#00BFBF")]
        )

    # ------------------------------------------------------------------
    # Métodos "placeholder" para enlazar con la lógica del controlador
    # ------------------------------------------------------------------
    def on_search_click(self):
        """Evento para el botón 'Buscar'."""
        print("Buscando ventas desde", self.start_date.get(), "hasta", self.end_date.get())
        # Aquí podrías llamar a un método del controlador 
        # para filtrar ventas y actualizar la tabla/labels
