# view/sales_view.py
import tkinter as tk
from tkinter import ttk

class SalesView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(width=800, height=600)
        self.create_widgets()
        self.pack(fill="both", expand=True)

    def create_widgets(self):
        turquesa = "#00BFBF"
        naranja = "#FFA500"
        fondo_blanco = "#FFFFFF"
        gris_claro = "#F0F0F0"
        verde = "#28A745"
        rojo = "#FF0000"
        azul = "#0000FF"
        gris_borde = "#D3D3D3"
        negro = "#000000"
        gris_texto = "#808080"
        blanco = "#FFFFFF"

        # Cabecera
        header_frame = tk.Frame(self, bg=turquesa, height=60)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)

        title_label = tk.Label(header_frame, text="Venta de Productos", fg=blanco, bg=turquesa,
                               font=("Sans-serif", 20, "bold"))
        title_label.pack(side="left", padx=20)

        volver_button = tk.Button(header_frame, text="Volver al Menú",
                                  bg=naranja, fg=negro,
                                  font=("Sans-serif", 14, "bold"),
                                  width=12, height=1,
                                  bd=0, highlightthickness=0,
                                  cursor="hand2",
                                  command=self.controller.show_login_view)
        volver_button.pack(side="right", padx=20)

        # Cuerpo principal
        main_frame = tk.Frame(self, bg=gris_claro)
        main_frame.pack(fill="both", expand=True)

        # Barra lateral a la derecha
        sidebar = tk.Frame(main_frame, bg=gris_claro)
        # Empaquetar primero el sidebar a la derecha, sin expand:
        sidebar.pack(side="right", fill="y", padx=20, pady=20)

        add_button = tk.Button(sidebar, text="Agregar Producto",
                               bg=verde, fg=blanco,
                               font=("Sans-serif",14,"bold"),
                               width=15, height=2,
                               bd=0, highlightthickness=0,
                               cursor="hand2")
        add_button.pack(pady=10)

        delete_button = tk.Button(sidebar, text="Eliminar Producto",
                                  bg=rojo, fg=blanco,
                                  font=("Sans-serif",14,"bold"),
                                  width=15, height=2,
                                  bd=0, highlightthickness=0,
                                  cursor="hand2")
        delete_button.pack(pady=10)

        summary_frame = tk.Frame(sidebar, bg=gris_claro)
        summary_frame.pack(pady=20, anchor="w")

        total_label = tk.Label(summary_frame, text="Total Venta: $ 0", bg=gris_claro, fg=negro,
                               font=("Sans-serif",16,"bold"))
        total_label.pack(anchor="w")

        recibe_label = tk.Label(summary_frame, text="Recibe:", bg=gris_claro, fg=negro,
                                font=("Sans-serif",14))
        recibe_label.pack(anchor="w", pady=(20,5))

        recibe_entry = tk.Entry(summary_frame, width=20, bd=1, fg=negro, bg=blanco)
        recibe_entry.pack(anchor="w")

        # Tabla a la izquierda
        table_frame = tk.Frame(main_frame, bg=fondo_blanco, bd=1, relief="solid")
        # Empaquetar table_frame a la izquierda con expand para que use el espacio restante:
        table_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        table_frame.pack_propagate(False)

        columns = ("codigo", "nombre", "valor", "cantidad")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("codigo", text="Código Producto")
        self.tree.heading("nombre", text="Nombre Producto")
        self.tree.heading("valor", text="Valor Producto")
        self.tree.heading("cantidad", text="Cantidad Producto")

        style = ttk.Style()
        style.configure("Treeview", background=blanco, foreground=negro, rowheight=25, fieldbackground=blanco)
        style.map('Treeview', background=[('selected', gris_claro)])

        self.tree.pack(fill="both", expand=True)
        self.tree.insert("", "end", values=("", "Tabla sin contenido", "", ""), tags=("placeholder",))
        self.tree.tag_configure("placeholder", foreground=gris_texto, anchor="center")

        # Sección inferior métodos de pago
        payment_frame = tk.Frame(self, bg=gris_claro, height=60)
        payment_frame.pack(side="bottom", fill="x")
        payment_frame.pack_propagate(False)

        payment_container = tk.Frame(payment_frame, bg=gris_claro)
        payment_container.place(relx=0.5, rely=0.5, anchor="center")

        efectivo_button = tk.Button(payment_container, text="Pago con Efectivo",
                                    bg=azul, fg=blanco,
                                    font=("Sans-serif",14,"bold"),
                                    width=20, height=2,
                                    bd=0, highlightthickness=0,
                                    cursor="hand2")
        efectivo_button.pack(side="left", padx=10)

        tarjeta_button = tk.Button(payment_container, text="Pago con Tarjeta",
                                   bg=azul, fg=blanco,
                                   font=("Sans-serif",14,"bold"),
                                   width=20, height=2,
                                   bd=0, highlightthickness=0,
                                   cursor="hand2")
        tarjeta_button.pack(side="left", padx=10)

        transferencia_button = tk.Button(payment_container, text="Transferencia",
                                         bg=azul, fg=blanco,
                                         font=("Sans-serif",14,"bold"),
                                         width=20, height=2,
                                         bd=0, highlightthickness=0,
                                         cursor="hand2")
        transferencia_button.pack(side="left", padx=10)
# view/sales_view.py
import tkinter as tk
from tkinter import ttk

class SalesView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(width=800, height=600)
        self.create_widgets()
        self.pack(fill="both", expand=True)

    def create_widgets(self):
        # Colores y demás omitidos por brevedad (usar los mismos que antes)...
        turquesa = "#00BFBF"
        naranja = "#FFA500"
        fondo_blanco = "#FFFFFF"
        gris_claro = "#F0F0F0"
        verde = "#28A745"
        rojo = "#FF0000"
        azul = "#0000FF"
        negro = "#000000"
        gris_texto = "#808080"
        blanco = "#FFFFFF"

        # Cabecera
        header_frame = tk.Frame(self, bg=turquesa, height=60)
        header_frame.pack(side="top", fill="x")  # Primero el header arriba
        header_frame.pack_propagate(False)

        title_label = tk.Label(header_frame, text="Venta de Productos", fg=blanco, bg=turquesa,
                               font=("Sans-serif", 20, "bold"))
        title_label.pack(side="left", padx=20)

        volver_button = tk.Button(header_frame, text="Volver al Menú",
                                  bg=naranja, fg=negro,
                                  font=("Sans-serif", 14, "bold"),
                                  width=12, height=1,
                                  bd=0, highlightthickness=0,
                                  cursor="hand2",
                                  command=self.controller.show_login_view)
        volver_button.pack(side="right", padx=20)

        # Sección inferior (payment_frame) para métodos de pago
        payment_frame = tk.Frame(self, bg=gris_claro, height=60)
        payment_frame.pack(side="bottom", fill="x")  # Luego el frame de pagos abajo
        payment_frame.pack_propagate(False)

        payment_container = tk.Frame(payment_frame, bg=gris_claro)
        payment_container.place(relx=0.5, rely=0.5, anchor="center")

        efectivo_button = tk.Button(payment_container, text="Pago con Efectivo",
                                    bg=azul, fg=blanco,
                                    font=("Sans-serif",14,"bold"),
                                    width=20, height=2,
                                    bd=0, highlightthickness=0,
                                    cursor="hand2")
        efectivo_button.pack(side="left", padx=10)

        tarjeta_button = tk.Button(payment_container, text="Pago con Tarjeta",
                                   bg=azul, fg=blanco,
                                   font=("Sans-serif",14,"bold"),
                                   width=20, height=2,
                                   bd=0, highlightthickness=0,
                                   cursor="hand2")
        tarjeta_button.pack(side="left", padx=10)

        transferencia_button = tk.Button(payment_container, text="Transferencia",
                                         bg=azul, fg=blanco,
                                         font=("Sans-serif",14,"bold"),
                                         width=20, height=2,
                                         bd=0, highlightthickness=0,
                                         cursor="hand2")
        transferencia_button.pack(side="left", padx=10)

        # Cuerpo principal (en el medio)
        main_frame = tk.Frame(self, bg=gris_claro)
        main_frame.pack(side="top", fill="both", expand=True)  
        # Nota: Ahora el main_frame está entre el header_frame (arriba) y el payment_frame (abajo).

        # Tabla a la izquierda
        table_frame = tk.Frame(main_frame, bg=fondo_blanco, bd=1, relief="solid")
        table_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        columns = ("codigo", "nombre", "valor", "cantidad")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("codigo", text="Código Producto")
        self.tree.heading("nombre", text="Nombre Producto")
        self.tree.heading("valor", text="Valor Producto")
        self.tree.heading("cantidad", text="Cantidad Producto")

        style = ttk.Style()
        style.configure("Treeview", background=blanco, foreground=negro, rowheight=25, fieldbackground=blanco)
        style.map('Treeview', background=[('selected', gris_claro)])

        self.tree.pack(fill="both", expand=True)
        self.tree.insert("", "end", values=("", "Tabla sin contenido", "", ""), tags=("placeholder",))
        self.tree.tag_configure("placeholder", foreground=gris_texto, anchor="center")

        # Barra lateral a la derecha
        sidebar = tk.Frame(main_frame, bg=gris_claro)
        sidebar.pack(side="right", fill="y", padx=20, pady=20)

        add_button = tk.Button(sidebar, text="Agregar Producto",
                               bg=verde, fg=blanco,
                               font=("Sans-serif",14,"bold"),
                               width=15, height=2,
                               bd=0, highlightthickness=0,
                               cursor="hand2")
        add_button.pack(pady=10)

        delete_button = tk.Button(sidebar, text="Eliminar Producto",
                                  bg=rojo, fg=blanco,
                                  font=("Sans-serif",14,"bold"),
                                  width=15, height=2,
                                  bd=0, highlightthickness=0,
                                  cursor="hand2")
        delete_button.pack(pady=10)

        summary_frame = tk.Frame(sidebar, bg=gris_claro)
        summary_frame.pack(pady=20, anchor="w")

        total_label = tk.Label(summary_frame, text="Total Venta: $ 0", bg=gris_claro, fg=negro,
                               font=("Sans-serif",16,"bold"))
        total_label.pack(anchor="w")

        recibe_label = tk.Label(summary_frame, text="Recibe:", bg=gris_claro, fg=negro,
                                font=("Sans-serif",14))
        recibe_label.pack(anchor="w", pady=(20,5))

        recibe_entry = tk.Entry(summary_frame, width=20, bd=1, fg=negro, bg=blanco)
        recibe_entry.pack(anchor="w")
