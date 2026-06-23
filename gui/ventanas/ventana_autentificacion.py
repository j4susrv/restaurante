import tkinter as tk
from tkinter import messagebox, ttk

class VentanaAutenticacion:
    def __init__(self, parent, callback_exito):
        self.win = tk.Toplevel(parent)
        self.win.title("Acceso Administrativo")
        self.win.geometry("300x200")
        self.win.grab_set() # Bloquea el resto hasta que se loguee o cierre
        self.callback = callback_exito
        
        ttk.Label(self.win, text="Usuario:").pack(pady=(15, 0))
        self.ent_user = ttk.Entry(self.win)
        self.ent_user.pack()
        
        ttk.Label(self.win, text="Contraseña:").pack(pady=(10, 0))
        self.ent_pass = ttk.Entry(self.win, show="*")
        self.ent_pass.pack()
        
        ttk.Button(self.win, text="Ingresar", command=self.verificar).pack(pady=20)

    def verificar(self):
        usuario = self.ent_user.get()
        password = self.ent_pass.get()
        
        # --- AQUÍ DEFINES LAS CREDENCIALES ---
        # Idealmente, esto debería venir de una base de datos o un archivo de config
        if usuario == "Xyi1820" and password == "restaurante1213%":
            self.win.destroy()
            self.callback() # Llama a la ventana de inventario
        else:
            messagebox.showerror("Acceso Denegado", "Usuario o contraseña incorrectos.")