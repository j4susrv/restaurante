"""
gui/vistas.py
Responsabilidad única: Métodos auxiliares de lectura y actualización
de las vistas (tablas Treeview y Listbox de detalles) en la ventana principal.
"""
import tkinter as tk
import repositorio
from utils_format import formato_moneda

PALABRAS_BEBIDA = ["cocacola", "pepsi", "monster", "té", "cafe", "café", "bebida", "fanta", "sprite", "jugo", "ml", "cc"]

class VistasPrincipales:
    """Gestiona la actualización y renderizado de los datos en las tablas de la ventana principal."""

    def __init__(self, sistema, tabla_pedidos, tabla_inventario, tabla_bebidas, lista_detalles):
        self.sistema = sistema
        self.tabla_pedidos = tabla_pedidos
        self.tabla_inventario = tabla_inventario
        self.tabla_bebidas = tabla_bebidas
        self.lista_detalles = lista_detalles

    def actualizar_tablas(self):
        """
        Limpia y recarga todas las tablas principales. 
        Este método fuerza la lectura desde el repositorio, actualizando los stocks calculados.
        """
        # 1. Limpiar vistas antiguas
        for item in self.tabla_pedidos.get_children(): self.tabla_pedidos.delete(item)
        for item in self.tabla_inventario.get_children(): self.tabla_inventario.delete(item)
        for item in self.tabla_bebidas.get_children(): self.tabla_bebidas.delete(item)

        # 2. Cargar datos frescos de pedidos
        pedidos = repositorio.cargarPedidos()
        for p in pedidos:
            subtotal = sum(plato.precio for plato in p.platos)
            total_final = subtotal + (p.boleta.propina if p.boleta else 0)
            
            if getattr(p, 'mesa2', None):
                mesas_texto = f"{p.mesa1.numero}, {p.mesa2.numero}"
            else:
                mesas_texto = f"{p.mesa1.numero}"

            fecha = getattr(p, 'created_at', '')
            self.tabla_pedidos.insert("", tk.END, values=(p.id, p.cliente, fecha, mesas_texto, p.estado, f"${formato_moneda(total_final)}"))

        # 3. Cargar platos y recargar stock (gracias a la @property en la clase Plato)
        platos = repositorio.cargarPlatos()
        for pl in platos:
            nombre_min = pl.nombre.lower()
            if any(palabra in nombre_min for palabra in PALABRAS_BEBIDA):
                self.tabla_bebidas.insert("", tk.END, values=(pl.nombre, f"${formato_moneda(pl.precio)}", f"{pl.stock} u."))
            else:
                self.tabla_inventario.insert("", tk.END, values=(pl.nombre, f"${formato_moneda(pl.precio)}", f"{pl.stock} u."))

    def refrescar_listbox_detalle(self, pedido_id):
        """Limpia y muestra el detalle de un pedido específico."""
        self.lista_detalles.delete(0, tk.END)
        pedido = self.sistema.pedidoService.verDetalle(pedido_id)

        self.lista_detalles.insert(tk.END, f"CLIENTE: {pedido.cliente}")
        if getattr(pedido, 'created_at', None):
            self.lista_detalles.insert(tk.END, f"FECHA: {pedido.created_at}")
        
        if getattr(pedido, 'mesa2', None):
            mesas_texto = f"N° {pedido.mesa1.numero} + N° {pedido.mesa2.numero}"
        else:
            mesas_texto = f"N° {pedido.mesa1.numero}"
            
        self.lista_detalles.insert(tk.END, f"MESA: {mesas_texto} | ESTADO: {pedido.estado.upper()}")
        if pedido.nota:
            self.lista_detalles.insert(tk.END, f"NOTA PEDIDO: {pedido.nota}")
        self.lista_detalles.insert(tk.END, "-" * 50)

        if not pedido.platos:
            self.lista_detalles.insert(tk.END, " (Sin consumos registrados aún) ")
            return

        for p in pedido.platos:
            linea = f"• {p.nombre:<22} ${formato_moneda(p.precio):>6}"
            if p.nota:
                linea += f"  -> (* {p.nota})"
            self.lista_detalles.insert(tk.END, linea)

        self.lista_detalles.insert(tk.END, "-" * 50)
        subtotal = sum(plato.precio for plato in pedido.platos)
        self.lista_detalles.insert(tk.END, f"SUBTOTAL COMIDAS:     ${formato_moneda(subtotal)}")

        if pedido.boleta:
            self.lista_detalles.insert(tk.END, f"PROPINA REGISTRADA:    ${formato_moneda(pedido.boleta.propina)}")
            self.lista_detalles.insert(tk.END, f"TOTAL DE LA COMPRA:    ${formato_moneda(pedido.boleta.total + pedido.boleta.propina)}")
            if pedido.boleta.divisiones:
                self.lista_detalles.insert(tk.END, f" [Dividido en {len(pedido.boleta.divisiones)} personas: ${formato_moneda(pedido.boleta.divisiones[0].monto)} c/u]")

    def actualizar_tabla_ingredientes(self, tabla_destino):
        """Limpia y rellena la tabla de insumos básicos usando el servicio."""
        for item in tabla_destino.get_children():
            tabla_destino.delete(item)

        if hasattr(self.sistema, 'bodegaService'):
            ingredientes = self.sistema.bodegaService.listarMateriasPrimas()
            for ing in ingredientes:
                tabla_destino.insert(
                    "", 
                    tk.END, 
                    values=(ing.nombre, f"{ing.stock_unidades} u.", ing.subcategoria, f"${ing.precio_unidad}")
                )