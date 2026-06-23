import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import os
from repositorio import cargarIngredientes

class VentanaInventario:
    def __init__(self, root, sistema, callback_actualizar=None):
        self.win = tk.Toplevel(root)
        self.win.title("Gestión de Inventario (Administrador)")
        self.win.geometry("400x400")
        self.win.grab_set() 
        self.sistema = sistema
        self.callback_actualizar = callback_actualizar
        
        ttk.Label(self.win, text="Administración de Stock", font=("Arial", 12, "bold")).pack(pady=10)
        
        self.ingredientes = cargarIngredientes()
        
        ttk.Label(self.win, text="Seleccione Insumo:").pack()
        self.cb_ingredientes = ttk.Combobox(self.win, state="readonly")
        self.cb_ingredientes['values'] = [i.nombre for i in self.ingredientes]
        self.cb_ingredientes.bind("<<ComboboxSelected>>", self.mostrar_stock_actual)
        self.cb_ingredientes.pack(pady=5)
        
        self.lbl_stock_actual = ttk.Label(self.win, text="Stock actual: -", font=("Arial", 10, "italic"))
        self.lbl_stock_actual.pack(pady=10)
        
        ttk.Label(self.win, text="Nuevo Stock:").pack(pady=5)
        self.ent_stock = ttk.Entry(self.win)
        self.ent_stock.pack()
        
        ttk.Button(self.win, text="Confirmar y Guardar", command=self.guardar_stock).pack(pady=20)

    def mostrar_stock_actual(self, event):
        nombre = self.cb_ingredientes.get()
        ing = next((i for i in self.ingredientes if i.nombre == nombre), None)
        if ing:
            self.lbl_stock_actual.config(text=f"Stock actual: {ing.stock_unidades} unidades")

    def guardar_stock(self):
        try:
            nombre = self.cb_ingredientes.get()
            if not nombre:
                messagebox.showwarning("Error", "Seleccione un ingrediente.")
                return
            
            nuevo_valor = int(self.ent_stock.get())
            self.sistema.inventarioService.ajustarStockIngredienteManual(nombre, nuevo_valor)
            
            # --- CORRECCIÓN 1: Recargar la lista en memoria ---
            self.ingredientes = cargarIngredientes()
            
            # --- CORRECCIÓN 2: Actualizar el label visual inmediatamente ---
            self.lbl_stock_actual.config(text=f"Stock actual: {nuevo_valor} unidades")
            
            # Log de auditoría
            if not os.path.exists("logs"): os.makedirs("logs")
            with open("logs/log_inventario.txt", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Ajuste: {nombre} -> {nuevo_valor}\n")
            
            # Disparamos el refresco de la tabla en la ventana principal
            if self.callback_actualizar:
                self.callback_actualizar()
            
            messagebox.showinfo("Éxito", f"Stock de {nombre} actualizado a {nuevo_valor}.")
            self.ent_stock.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))