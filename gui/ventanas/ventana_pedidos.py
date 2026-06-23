"""
gui/ventanas/ventana_pedidos.py
Responsabilidad única: Ventanas emergentes para abrir un pedido,
agregar consumos y editar/eliminar platos ya agregados (Flujos 1, 2, 3).
"""
import tkinter as tk
from tkinter import messagebox, ttk
import repositorio
from gui.validadores_gui import ValidadoresGUI
from utils_format import formato_moneda


class VentanaPedidos:
    """Gestiona todas las ventanas relacionadas con el ciclo de vida de los platos en un pedido."""

    def __init__(self, root, sistema, actualizar_tablas_callback, refrescar_detalle_callback):
        self.root = root
        self.sistema = sistema
        self._actualizar_tablas = actualizar_tablas_callback
        self._refrescar_detalle = refrescar_detalle_callback

    # =====================================================================
    # FLUJO 1: ABRIR PEDIDO CONTROLES
    # =====================================================================
    def abrir_pedido(self):
        win = tk.Toplevel(self.root)
        win.title("Abrir Nuevo Pedido (Max 2 Mesas)")
        win.geometry("400x350")
        win.grab_set()
        
        val_cmd = ValidadoresGUI.crear_validador_texto_cliente(win)
        ttk.Label(win, text="Nombre del Cliente:", font=("Arial", 10, "bold")).pack(pady=(15, 2))
        
        ent_cliente = ttk.Entry(
            win,
            width=30,
            validate="key",
            validatecommand=(val_cmd, "%P")
        )
        ent_cliente.pack(pady=5)
        ent_cliente.focus()
        
        ttk.Label(win, text="Seleccione Mesa(s) Disponibles (Máx 2):\n(Use Ctrl para seleccionar más de una)",
                  font=("Arial", 9, "bold"), justify=tk.CENTER).pack(pady=5)
        
        frame_list = ttk.Frame(win)
        frame_list.pack(pady=5)
        listbox_mesas = tk.Listbox(frame_list, selectmode=tk.MULTIPLE, height=5, width=30, exportselection=0)
        listbox_mesas.pack(side=tk.LEFT)
        scrollbar = ttk.Scrollbar(frame_list, orient=tk.VERTICAL, command=listbox_mesas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox_mesas.config(yscrollcommand=scrollbar.set)
        
        mesas_datos = [m for m in repositorio.cargarMesas() if not m.ocupada]
        for m in mesas_datos:
            listbox_mesas.insert(tk.END, f"Mesa {m.numero} (Capacidad: {m.capacidad})")

        def procesar():
            try:
                cliente = ent_cliente.get().strip()
                self.sistema.validador_service.validarCliente(cliente)
                indices_seleccionados = listbox_mesas.curselection()
                if not indices_seleccionados:
                    raise ValueError("Debe seleccionar al menos una mesa para el cliente.")
                if len(indices_seleccionados) > 2:
                    raise ValueError("No está permitido seleccionar más de 2 mesas para una sola cuenta.")
                
                # Extraemos los números de las mesas seleccionadas
                numeros_a_reservar = [mesas_datos[idx].numero for idx in indices_seleccionados]
                
                # REPARADO: Se envía la lista original de números directo al manager.
                pedido = self.sistema.pedidoService.crearPedido(cliente, numeros_a_reservar)
                
                mesas_texto = ", ".join(map(str, numeros_a_reservar))
                messagebox.showinfo("Éxito", f"Pedido #{pedido.id} abierto exitosamente en las mesas [{mesas_texto}]")
                win.destroy()
                self._actualizar_tablas()
            except ValueError as e:
                messagebox.showerror("Error de Validation", str(e))

        ttk.Button(win, text="Confirmar Apertura", command=procesar).pack(pady=15)

    # =====================================================================
    # FLUJO 2: AGREGAR PLATO O BEBESTIBLE AL PEDIDO (SEPARADOS)
    # =====================================================================
    def agregar_plato(self, pedido_id):
        win = tk.Toplevel(self.root)
        win.title(f"Añadir Consumo - Pedido #{pedido_id}")
        win.geometry("450x320")
        win.grab_set()

        todos_los_items = self.sistema.menuService.listarPlatosDisponibles()
        comidas = []
        bebestibles = []
        palabras_bebida = ["cocacola", "pepsi", "monster", "té", "cafe", "café", "bebida", "fanta", "sprite", "jugo", "ml", "cc"]

        for item in todos_los_items:
            if any(p in item.nombre.lower() for p in palabras_bebida):
                bebestibles.append(item.nombre)
            else:
                comidas.append(item.nombre)

        ttk.Label(win, text="🍽️ Seleccionar Plato o Comida:", font=("Arial", 9, "bold")).pack(pady=(15, 2))
        cb_comidas = ttk.Combobox(win, values=comidas, state="readonly", width=38)
        cb_comidas.pack(pady=2)
        if comidas: cb_comidas.current(0)

        def añadir_comida():
            try:
                nombre = cb_comidas.get()
                if not nombre: raise ValueError("Seleccione una comida válida.")
                self.sistema.pedidoService.agregarPlato(pedido_id, nombre)
                messagebox.showinfo("Agregado", f"Se añadió '{nombre}' con éxito.")
                self._actualizar_tablas()
                self._refrescar_detalle(pedido_id)
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(win, text="Agregar Plato Seleccionado", command=añadir_comida).pack(pady=(2, 15))

        ttk.Label(win, text="🥤 Seleccionar Bebestible / Líquido:", font=("Arial", 9, "bold")).pack(pady=(10, 2))
        cb_bebidas = ttk.Combobox(win, values=bebestibles, state="readonly", width=38)
        cb_bebidas.pack(pady=2)
        if bebestibles: cb_bebidas.current(0)

        def añadir_bebida():
            try:
                nombre = cb_bebidas.get()
                if not nombre: raise ValueError("Seleccione una bebida válida.")
                self.sistema.pedidoService.agregarPlato(pedido_id, nombre)
                messagebox.showinfo("Agregado", f"Se añadió '{nombre}' con éxito.")
                self._actualizar_tablas()
                self._refrescar_detalle(pedido_id)
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(win, text="Agregar Bebida Seleccionada", command=añadir_bebida).pack(pady=(2, 15))

    # =====================================================================
    # FLUJO 3: EDITAR / ELIMINAR PLATOS YA AGREGADOS
    # =====================================================================
    def editar_platos(self, pedido_id):
        pedido = self.sistema.pedidoService.verDetalle(pedido_id)
        if pedido.estado != "abierto":
            messagebox.showwarning("Atención", "Este pedido ya no se puede modificar por su estado.")
            return
        if not pedido.platos:
            messagebox.showwarning("Vacío", "El pedido no cuenta con platos para modificar.")
            return

        win = tk.Toplevel(self.root)
        win.title(f"Modificar Platos - Pedido #{pedido_id}")
        win.geometry("450x320")
        win.grab_set()

        ttk.Label(win, text="1. Seleccione el plato actual del cliente:", font=("Arial", 9, "bold")).pack(pady=(10, 2))
        items_actuales = [f"[{i}] {p.nombre} (${formato_moneda(p.precio)})" for i, p in enumerate(pedido.platos)]
        cb_items = ttk.Combobox(win, values=items_actuales, state="readonly", width=45)
        cb_items.pack(pady=5)
        cb_items.current(0)

        ttk.Label(win, text="2. Si desea MODIFICAR, elija el reemplazo chileno:", font=("Arial", 9, "bold")).pack(pady=(10, 2))
        platos_menu = [p.nombre for p in self.sistema.menuService.listarPlatosDisponibles()]
        cb_reemplazo = ttk.Combobox(win, values=platos_menu, state="readonly", width=45)
        cb_reemplazo.pack(pady=5)
        if platos_menu: cb_reemplazo.current(0)

        def ejecutar_modificar():
            try:
                idx = cb_items.current()
                nuevo_plato = cb_reemplazo.get()
                self.sistema.pedidoService.modificarPlato(pedido_id, idx, nuevo_plato)
                messagebox.showinfo("Éxito", "Plato reemplazado exitosamente.")
                win.destroy()
                self._actualizar_tablas()
                self._refrescar_detalle(pedido_id)
            except (ValueError, IndexError) as e:
                messagebox.showerror("Error", str(e))

        def ejecutar_eliminar():
            try:
                idx = cb_items.current()
                self.sistema.pedidoService.eliminarPlato(pedido_id, idx)
                messagebox.showinfo("Éxito", "Plato eliminado del pedido.")
                win.destroy()
                self._actualizar_tablas()
                self._refrescar_detalle(pedido_id)
            except (ValueError, IndexError) as e:
                messagebox.showerror("Error", str(e))

        btn_frame = ttk.Frame(win, padding=10)
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="Aplicar Cambio ", command=ejecutar_modificar).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Eliminar Plato ", command=ejecutar_eliminar).pack(side=tk.LEFT, padx=10)