# view/login_view.py
import tkinter as tk
from PIL import Image, ImageTk
import os

class LoginView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(width=800, height=600)
        self.create_widgets()
        self.pack(fill="both", expand=True)

    def create_widgets(self):
        # Colores
        turquesa = "#00BFBF"
        naranja = "#FF9900"
        marron_oscuro = "#663300"
        fondo_blanco = "#FFFFFF"

        total_width = 800
        left_width = int(total_width * 0.35)  # 35% del ancho
        left_frame = tk.Frame(self, bg=turquesa, width=left_width, height=600)
        left_frame.pack(side="left", fill="y")
        left_frame.pack_propagate(False)

        container_left = tk.Frame(left_frame, bg=turquesa)
        container_left.place(relx=0.5, rely=0.5, anchor="center")

        title_text = "¡Bienvenido a\nConnie Pet Shop!"
        title_label = tk.Label(container_left, text=title_text, 
                               font=("Sans-serif", 18, "bold"), fg="#000000", bg=turquesa)
        title_label.pack(pady=30)

        # Config base botones
        btn_config = {
            "width": 20,
            "height": 2,
            "bg": naranja,
            "fg": "#FFFFFF",
            "font": ("Sans-serif", 14, "bold"),
            "bd": 0,
            "highlightthickness": 0,
            "activebackground": "#cc7a00",
            "cursor": "hand2"
        }

        # Botón "Ingreso a Ventas" -> show_sales_view()
        ventas_button = tk.Button(container_left, text="Ingreso a Ventas", **btn_config,
                                  command=self.controller.show_sales_view)
        ventas_button.pack(pady=10)

        # Botón "Control de Inventario" -> show_admin_view() (o product_management_view si así lo prefieres)
        inventario_button = tk.Button(container_left, text="Control de Inventario", **btn_config,
                                      command=self.controller.show_admin_view)
        inventario_button.pack(pady=10)

        # Botón "Reporte de Ventas" -> show_sales_report_view()
        reporte_button = tk.Button(container_left, text="Reporte de Ventas", **btn_config,
                                   command=self.controller.show_sales_report_view)
        reporte_button.pack(pady=10)

        # Botón "Salir" -> cerrar la aplicación (self.controller.root.destroy() asumiendo que main_controller tiene acceso)
        exit_button = tk.Button(container_left, text="Salir", 
                                width=10, height=1,
                                bg=marron_oscuro, fg="#FFFFFF",
                                font=("Sans-serif", 14),
                                bd=0, highlightthickness=0,
                                cursor="hand2",
                                command=self.exit_app)
        exit_button.pack(pady=10)

        # Sección derecha
        right_width = total_width - left_width
        right_frame = tk.Frame(self, bg=fondo_blanco, width=right_width, height=600)
        right_frame.pack(side="left", fill="both", expand=True)
        right_frame.pack_propagate(False)

        logo_container = tk.Frame(right_frame, width=200, height=200, 
                                  bg=fondo_blanco, bd=0,
                                  highlightbackground=turquesa,
                                  highlightcolor=turquesa,
                                  highlightthickness=2)
        logo_container.place(relx=0.5, rely=0.5, anchor="center")

        logo_path = "images/logo.png"
        abs_path = os.path.abspath(logo_path)
        print("Buscando imagen en:", abs_path)

        if os.path.exists(logo_path):
            # Cargamos imagen sin try/except para ver error si lo hay
            img = Image.open(logo_path)
            # Si PIL es muy reciente, ANTIALIAS se cambió por Image.Resampling.LANCZOS:
            img = img.resize((500, 500), Image.Resampling.LANCZOS)
            logo_img = ImageTk.PhotoImage(img)
            logo_label = tk.Label(logo_container, image=logo_img, bg=fondo_blanco)
            logo_label.image = logo_img  # Mantener referencia
            logo_label.pack(expand=True)
        else:
            print("No se encontró la imagen en la ruta:", abs_path)
            no_logo_label = tk.Label(logo_container, text="LOGO", bg=fondo_blanco, fg=turquesa, font=("Arial", 20))
            no_logo_label.pack(expand=True)

    def exit_app(self):
        # Cerrar la ventana principal (root)
        self.controller.root.destroy()
