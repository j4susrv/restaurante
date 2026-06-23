"""
gui/ventanas/ventana_bodega.py
Responsabilidad única: Ventana emergente para visualizar el stock crudo
de la bodega de ingredientes sin interferir con el menú (SRP).
"""
import tkinter as tk
from tkinter import ttk

class VentanaBodega:
    """Gestiona la interfaz modal para revisar las materias primas del restaurante."""

    def __init__(self, root, sistema, actualizar_ingredientes_callback):
        self.root = root
        self.sistema = sistema
        self._actualizar_ingredientes = actualizar_ingredientes_callback

    def abrir_bodega(self):
        """Despliega un modal interactivo con la lista de ingredientes base."""
        win = tk.Toplevel(self.root)
        win.title("Bodega de Materias Primas - Sabores de Chile")
        win.geometry("550x400")
        win.grab_set()  # Bloquea la ventana de atrás para evitar conflictos

        # Encabezado descriptivo
        lbl_titulo = ttk.Label(
            win, 
            text="Control de Stock Crudo e Ingredientes Base", 
            font=("Arial", 12, "bold"),
            foreground="#2C3E50"
        )
        lbl_titulo.pack(pady=10)

        # Contenedor para la tabla y su barra de desplazamiento
        frame_tabla = ttk.Frame(win, padding=10)
        frame_tabla.pack(fill=tk.BOTH, expand=True)

        scroll = ttk.Scrollbar(frame_tabla)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Estructura del Treeview basada en los atributos exactos de tu Dataclass
        # Columnas: Nombre, Stock, Subcategoría, Precio por Unidad
        columnas = ("nombre", "stock", "subcategoria", "precio")
        tabla = ttk.Treeview(
            frame_tabla, 
            columns=columnas, 
            show="headings", 
            yscrollcommand=scroll.set
        )
        scroll.config(command=tabla.yview)

        # Configurar cabeceras de columnas chilenas tradicionales
        tabla.heading("nombre", text="Ingrediente Base")
        tabla.heading("stock", text="Stock Disponible")
        tabla.heading("subcategoria", text="Subcategoría")
        tabla.heading("precio", text="Precio Costo U.")

        # Ajustar anchos
        tabla.column("nombre", width=180, anchor=tk.W)
        tabla.column("stock", width=110, anchor=tk.CENTER)
        tabla.column("subcategoria", width=110, anchor=tk.CENTER)
        tabla.column("precio", width=110, anchor=tk.E)

        tabla.pack(fill=tk.BOTH, expand=True)

        # Botón para cerrar de forma limpia
        btn_cerrar = ttk.Button(win, text="Cerrar Panel", command=win.destroy)
        btn_cerrar.pack(pady=10)

        # SOLID: Mandamos a rellenar la tabla usando el método desacoplado de VistasPrincipales
        self._actualizar_ingredientes(tabla)