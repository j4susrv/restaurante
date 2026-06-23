"""
gui/ventanas/ventana_factura.py
Responsabilidad única: Ventanas emergentes para generar boleta,
dividir cuenta y cancelar un pedido (Flujos 5 y 6).
"""
import tkinter as tk
from tkinter import messagebox, ttk
import repositorio
from utils_format import formato_moneda


class VentanaFactura:
    """Gestiona las ventanas de cierre de cuenta y cancelación de pedidos."""

    def __init__(self, root, sistema, actualizar_tablas_callback, refrescar_detalle_callback):
        self.root = root
        self.sistema = sistema
        self._actualizar_tablas = actualizar_tablas_callback
        self._refrescar_detalle = refrescar_detalle_callback

    # =====================================================================
    # FLUJO 5: GENERAR BOLETA & DIVIDIR CUENTAS
    # =====================================================================
    def facturar_pedido(self, pedido_id):
        pedido = self.sistema.pedidoService.verDetalle(pedido_id)
        if pedido.estado != "abierto":
            messagebox.showwarning("Facturado", "Este pedido ya se encuentra cerrado o cancelado.")
            return
        if not pedido.platos:
            messagebox.showwarning("Sin Consumo", "No se puede cobrar un pedido sin platos asignados.")
            return

        win = tk.Toplevel(self.root)
        win.title(f"Cierre de Cuenta - Pedido #{pedido_id}")
        win.geometry("450x420")
        win.grab_set()

        subtotal = self.sistema.pedidoService.calcularTotal(pedido_id)

        ttk.Label(win, text=f"Monto Subtotal de Platos: ${formato_moneda(subtotal)}", font=("Arial", 11, "bold"), foreground="#16A085").pack(pady=10)

        ttk.Label(win, text="Tipo de Pago Principal:", font=("Arial", 9, "bold")).pack()
        cb_pago = ttk.Combobox(win, values=["efectivo", "tarjeta", "transferencia"], state="readonly")
        cb_pago.pack(pady=5)
        cb_pago.current(0)

        ttk.Label(win, text="Monto de Propina Sugerida (Pesos $):", font=("Arial", 9, "bold")).pack()
        ent_propina = ttk.Entry(win, width=15)
        ent_propina.pack(pady=5)
        ent_propina.insert(0, str(int(subtotal * 0.10)))

        capacidad_total = pedido.mesa1.capacidad + (pedido.mesa2.capacidad if pedido.mesa2 else 0)

        div_frame = ttk.LabelFrame(win, text=" ¿Dividir Cuenta entre Amigos? (Opcional) ", padding=10)
        div_frame.pack(fill=tk.X, padx=15, pady=10)

        ttk.Label(div_frame, text="N° Personas:").grid(row=0, column=0, padx=5)
        spin_pers = ttk.Spinbox(div_frame, from_=1, to=max(1, capacidad_total), width=5, state="readonly")
        spin_pers.set(1)
        spin_pers.grid(row=0, column=1, padx=5)

        def procesar_pago():
            try:
                # Obtención de datos
                tipo_pago = cb_pago.get()
                propina_str = ent_propina.get().strip()
                
                # Validación de entrada
                if not propina_str.isdigit():
                    raise ValueError("La propina debe ser un número entero.")
                
                monto_propina = int(propina_str)
                if monto_propina <= 0:
                    raise ValueError("El monto de la propina debe ser mayor a 0.")
                
                personas = int(spin_pers.get())
                se_divide = (personas > 1)

                # Ejecución de lógica de negocio (Facturación + División)
                boleta = self.sistema.facturaService.generarBoleta(
                    pedido_id, tipo_pago, monto_propina, dividir=se_divide
                )

                if se_divide:
                    self.sistema.divisionService.dividirCuenta(pedido_id, personas, [tipo_pago])
                
                messagebox.showinfo("Éxito", "Pago procesado correctamente.")
                win.destroy()
                self._actualizar_tablas()
                self._refrescar_detalle(pedido_id)
            
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(win, text="Efectuar Pago e Imprimir", command=procesar_pago).pack(pady=15)

    # =====================================================================
    # FLUJO 6: CANCELAR PEDIDO TOTAL
    # =====================================================================
    def cancelar_pedido(self, pedido_id):
        if messagebox.askyesno("Confirmar", f"¿Está absolutamente seguro de cancelar el pedido #{pedido_id}?\nEsta acción devolverá los ingredientes al inventario y cerrará el registro."):
            try:
                self.sistema.pedidoService.cancelarPedido(pedido_id)
                messagebox.showinfo("Cancelado", f"El pedido #{pedido_id} fue anulado con éxito.")
                self._actualizar_tablas()
                self._refrescar_detalle(pedido_id)
            except ValueError as e:
                messagebox.showerror("Error", str(e))