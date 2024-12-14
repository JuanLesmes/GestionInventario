import tkinter as tk
from controller.main_controller import MainController

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")  # Tamaño inicial suficiente para ver el contenido
    app = MainController(root)
    root.mainloop()
