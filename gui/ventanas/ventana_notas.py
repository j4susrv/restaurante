"""
gui/ventanas/ventana_notas.py
Responsabilidad única: Ventana emergente para gestionar notas
de cocina del pedido y de platos individuales (Flujo 4).
"""
import tkinter as tk
from tkinter import messagebox, ttk
from gui.validadores_gui import ValidadoresGUI


class VentanaNotas:
    """Gestiona la ventana de notas de cocina de un pedido."""

    def __init__(self, root, sistema, refrescar_detalle_callback):
        self.root = root
        self.sistema = sistema
        self._refrescar_detalle = refrescar_detalle_callback

    # =====================================================================
    # FLUJO 4: AGREGAR NOTAS ESPECÍFICAS
    # =====================================================================
    def gestionar_notas(self, pedido_id):
        pedido = self.sistema.pedidoService.verDetalle(pedido_id)
        if pedido.estado != "abierto":
            messagebox.showwarning("Denegado", "El pedido no está abierto.")
            return

        win = tk.Toplevel(self.root)
        win.title("Gestión de Notas de Cocina")
        win.geometry("400x260")
        win.grab_set()

        # CAMBIO: Conectamos el validador estricto a las entradas de texto
        val_notas_cmd = ValidadoresGUI.crear_validador_notas(win)

        ttk.Label(win, text="Nota General para todo el Pedido:", font=("Arial", 9, "bold")).pack(pady=(10, 2))

        # Conectamos el validador a la nota general
        ent_nota_ped = ttk.Entry(
            win,
            width=42,
            validate="key",
            validatecommand=(val_notas_cmd, "%P")
        )
        ent_nota_ped.pack(pady=2)
        ent_nota_ped.insert(0, pedido.nota)

        ttk.Label(win, text="O añadir nota a un plato específico del pedido:", font=("Arial", 9, "bold")).pack(pady=(15, 2))
        platos_p = [f"[{i}] {p.nombre}" for i, p in enumerate(pedido.platos)]
        cb_platos_p = ttk.Combobox(win, values=platos_p, state="readonly", width=40)
        cb_platos_p.pack(pady=2)
        if platos_p: cb_platos_p.current(0)

        # Conectamos el validador a la nota del plato individual
        ent_nota_plat = ttk.Entry(
            win,
            width=42,
            validate="key",
            validatecommand=(val_notas_cmd, "%P")
        )
        ent_nota_plat.pack(pady=5)

        def guardar_todo():
            try:
                nota_p = ent_nota_ped.get().strip()
                self.sistema.pedidoService.agregarNotaPedido(pedido_id, nota_p)

                if platos_p and ent_nota_plat.get().strip():
                    idx = cb_platos_p.current()
                    self.sistema.pedidoService.agregarNotaPlato(pedido_id, idx, ent_nota_plat.get().strip())

                messagebox.showinfo("Guardado", "Notas asignadas a cocina.")
                win.destroy()
                self._refrescar_detalle(pedido_id)
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(win, text="Guardar Notas", command=guardar_todo).pack(pady=15)