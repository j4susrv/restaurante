#Se orquesta toda la interfaz grafica
import tkinter as tk
from tkinter import messagebox, ttk

from gui.vistas import VistasPrincipales
from gui.ventanas.ventana_pedidos import VentanaPedidos
from gui.ventanas.ventana_notas import VentanaNotas
from gui.ventanas.ventana_factura import VentanaFactura
from gui.ventanas.ventana_bodega import VentanaBodega
from gui.ventanas.ventana_autentificacion import VentanaAutenticacion
from gui.ventanas.ventana_inventario import VentanaInventario

class RestauranteGUI:
    def __init__(self, root, sistema):
        self.root = root
        self.sistema = sistema
        self.root.title("Gestión Gastronómica - Sabores de Chile")
        self.root.geometry("900x650")  # Ajustado un poco el alto para las dos tablas
        self.root.minsize(800, 550)

        # Estilos visuales atractivos
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Arial", 10, "bold"), padding=6)
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"), foreground="#2C3E50")

        self._crear_interfaz_principal()

        # Inyectamos las vistas ya construidas 
        self._vistas = VistasPrincipales(
            self.sistema,
            self.tabla_pedidos,
            self.tabla_inventario,
            self.tabla_bebidas,
            self.lista_detalles,
            getattr(self, 'tabla_notificaciones', None)
        )

        # Instanciamos los controladores de ventanas, pasando lo necesario
        self._vent_pedidos = VentanaPedidos(
            self.root, self.sistema,
            self._vistas.actualizar_tablas,
            self._vistas.refrescar_listbox_detalle
        )
        self._vent_notas = VentanaNotas(
            self.root, self.sistema,
            self._vistas.refrescar_listbox_detalle
        )
        self._vent_factura = VentanaFactura(
            self.root, self.sistema,
            self._vistas.actualizar_tablas,
            self._vistas.refrescar_listbox_detalle
        )
        # NUEVO: Instancia del controlador de la ventana de materias primas
        self._vent_bodega = VentanaBodega(
            self.root, self.sistema,
            self._vistas.actualizar_tabla_ingredientes
        )
        self.actualizar_tablas()

        # Programar refresco periódico de tablas (incluye notificaciones)
        try:
            self.root.after(30000, self.actualizar_tablas)
        except Exception:
            pass

    def _crear_interfaz_principal(self):
        # Contenedor con scroll vertical para toda la interfaz
        container = ttk.Frame(self.root)
        container.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(container, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.scrollable_frame = ttk.Frame(self.canvas)
        self._canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind(
            "<Configure>",
            lambda event: self.canvas.itemconfig(self._canvas_window, width=event.width)
        )

        # Contenedor principal dentro del canvas scrollable
        main_frame = ttk.Frame(self.scrollable_frame, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- SECCIÓN SUPERIOR: BOTONES DE ACCIÓN MÓDULO ---
        acciones_frame = ttk.LabelFrame(main_frame, text=" Operaciones del Sistema ", padding=10)
        acciones_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Button(acciones_frame, text="Abrir Pedido", command=self.ventana_abrir_pedido).pack(side=tk.LEFT, padx=5)
        ttk.Button(acciones_frame, text="Agregar Consumo", command=self.ventana_agregar_plato).pack(side=tk.LEFT, padx=5)
        ttk.Button(acciones_frame, text="Modificar/Eliminar", command=self.ventana_editar_platos).pack(side=tk.LEFT, padx=5)
        ttk.Button(acciones_frame, text="Notas", command=self.ventana_gestionar_notas).pack(side=tk.LEFT, padx=5)
        ttk.Button(acciones_frame, text="Cerrar / Facturar", command=self.ventana_facturar_pedido).pack(side=tk.LEFT, padx=5)
        ttk.Button(acciones_frame, text="Cancelar Pedido", command=self.accion_cancelar_pedido).pack(side=tk.LEFT, padx=5)
        ttk.Button(acciones_frame, text="Ver Bodega", command=self.ventana_revisar_bodega).pack(side=tk.LEFT, padx=5)
        ttk.Button(acciones_frame, text="Admin Stock", command=self.abrir_admin_stock, style="Admin.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(acciones_frame, text="Borrar Aviso", command=self.borrar_aviso).pack(side=tk.LEFT, padx=5)
        # --- SECCIÓN CENTRAL: TABLAS DE MONITOREO EN VIVO ---
        paneles_frame = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paneles_frame.pack(fill=tk.BOTH, expand=True)

        # Panel Izquierdo: Pedidos Activos
        pedidos_lf = ttk.LabelFrame(paneles_frame, text=" Pedidos en Curso ", padding=5)
        paneles_frame.add(pedidos_lf, weight=3)

        # Agregado: columna Fecha de Creación visible en la tabla de pedidos
        self.tabla_pedidos = ttk.Treeview(pedidos_lf, columns=("id", "cliente", "fecha", "mesa", "estado", "total"), show="headings")
        self.tabla_pedidos.heading("id", text="ID Pedido")
        self.tabla_pedidos.heading("cliente", text="Cliente")
        self.tabla_pedidos.heading("fecha", text="Fecha")
        self.tabla_pedidos.heading("mesa", text="Mesa N°")
        self.tabla_pedidos.heading("estado", text="Estado")
        self.tabla_pedidos.heading("total", text="Monto Total")
        self.tabla_pedidos.column("id", width=70, anchor=tk.CENTER)
        self.tabla_pedidos.column("fecha", width=100, anchor=tk.CENTER)
        self.tabla_pedidos.column("estado", width=100, anchor=tk.CENTER)
        self.tabla_pedidos.column("mesa", width=80, anchor=tk.CENTER)

        scroll_p = ttk.Scrollbar(pedidos_lf, orient=tk.VERTICAL, command=self.tabla_pedidos.yview)
        self.tabla_pedidos.configure(yscrollcommand=scroll_p.set)
        self.tabla_pedidos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_p.pack(side=tk.RIGHT, fill=tk.Y)

        self.tabla_pedidos.bind("<<TreeviewSelect>>", self.mostrar_detalle_seleccionado)

        # --- PANEL DERECHO: DETALLES Y DOS TABLAS DE STOCK SEPARADAS ---
        derecho_frame = ttk.Frame(paneles_frame)
        paneles_frame.add(derecho_frame, weight=2)

        # Detalle de Platos del Pedido Seleccionado
        detalle_lf = ttk.LabelFrame(derecho_frame, text=" Platos e Ítems Incluidos en el Pedido ", padding=5)
        detalle_lf.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        self.lista_detalles = tk.Listbox(detalle_lf, font=("Courier", 10), bg="#F8F9F9")
        self.lista_detalles.pack(fill=tk.BOTH, expand=True)

        # CAMBIO: TABLA 1 - Stock de Platos y Comidas
        comidas_lf = ttk.LabelFrame(derecho_frame, text=" Menú de Platos y Comidas ", padding=5)
        comidas_lf.pack(fill=tk.BOTH, expand=True, pady=2)

        self.tabla_inventario = ttk.Treeview(comidas_lf, columns=("nombre", "precio", "stock"), show="headings", height=4)
        self.tabla_inventario.heading("nombre", text="Plato Típico")
        self.tabla_inventario.heading("precio", text="Precio")
        self.tabla_inventario.heading("stock", text="Stock")
        self.tabla_inventario.column("precio", width=80, anchor=tk.E)
        self.tabla_inventario.column("stock", width=60, anchor=tk.CENTER)
        self.tabla_inventario.pack(fill=tk.BOTH, expand=True)

        # CAMBIO: TABLA 2 - Stock de Bebestibles (Nueva sección abajo)
        bebidas_lf = ttk.LabelFrame(derecho_frame, text=" Menú de Bebestibles y Líquidos ", padding=5)
        bebidas_lf.pack(fill=tk.BOTH, expand=True, pady=(2, 0))

        self.tabla_bebidas = ttk.Treeview(bebidas_lf, columns=("nombre", "precio", "stock"), show="headings", height=4)
        self.tabla_bebidas.heading("nombre", text="Bebida / Jugo / Café")
        self.tabla_bebidas.heading("precio", text="Precio")
        self.tabla_bebidas.heading("stock", text="Stock")
        self.tabla_bebidas.column("precio", width=80, anchor=tk.E)
        self.tabla_bebidas.column("stock", width=60, anchor=tk.CENTER)
        self.tabla_bebidas.pack(fill=tk.BOTH, expand=True)

        # Zona de Notificaciones / Avisos
        notifs_lf = ttk.LabelFrame(derecho_frame, text=" Notificaciones / Avisos ", padding=5)
        notifs_lf.pack(fill=tk.BOTH, expand=True, pady=(2, 0))
        self.tabla_notificaciones = ttk.Treeview(notifs_lf, columns=("tipo","mensaje","fecha","estado"), show="headings", height=4)
        self.tabla_notificaciones.heading("tipo", text="Tipo")
        self.tabla_notificaciones.heading("mensaje", text="Mensaje")
        self.tabla_notificaciones.heading("fecha", text="Fecha/Hora")
        self.tabla_notificaciones.heading("estado", text="Estado")
        self.tabla_notificaciones.column("tipo", width=100, anchor=tk.CENTER)
        self.tabla_notificaciones.column("fecha", width=140, anchor=tk.CENTER)
        self.tabla_notificaciones.column("estado", width=80, anchor=tk.CENTER)
        self.tabla_notificaciones.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll_alert = ttk.Scrollbar(notifs_lf, orient=tk.VERTICAL, command=self.tabla_notificaciones.yview)
        self.tabla_notificaciones.configure(yscrollcommand=scroll_alert.set)
        scroll_alert.pack(side=tk.RIGHT, fill=tk.Y)

        self.tabla_notificaciones.bind("<Double-1>", self.mostrar_alerta_detalle)

    #Son los metodos fuente, que delegan todo a los controladores especializados
    def ventana_abrir_pedido(self):
        self._vent_pedidos.abrir_pedido()

    def ventana_agregar_plato(self):
        pedido_id = self._obtener_id_seleccionado()
        if not pedido_id: return
        self._vent_pedidos.agregar_plato(pedido_id)

    def ventana_editar_platos(self):
        pedido_id = self._obtener_id_seleccionado()
        if not pedido_id: return
        self._vent_pedidos.editar_platos(pedido_id)

    def ventana_gestionar_notas(self):
        pedido_id = self._obtener_id_seleccionado()
        if not pedido_id: return
        self._vent_notas.gestionar_notas(pedido_id)

    def ventana_facturar_pedido(self):
        pedido_id = self._obtener_id_seleccionado()
        if not pedido_id: return
        self._vent_factura.facturar_pedido(pedido_id)

    def accion_cancelar_pedido(self):
        pedido_id = self._obtener_id_seleccionado()
        if not pedido_id: return
        self._vent_factura.cancelar_pedido(pedido_id)
    # NUEVO: Método orquestador para abrir de manera independiente el modal de bodega
    def ventana_revisar_bodega(self):
        """Abre el panel modal independiente de la bodega de ingredientes."""
        self._vent_bodega.abrir_bodega()
    def abrir_admin_stock(self):
        """
        Pasa la función de refresco a través de la autenticación 
        hasta llegar a la ventana de inventario.
        """
        # Definimos qué ventana abrir y qué función ejecutar después
        def abrir_inventario():
            # CORREGIDO: Usamos self._vistas (como se definió en el __init__)
            VentanaInventario(self.root, self.sistema, callback_actualizar=self._vistas.actualizar_tablas)
        
        # Pasamos el comando a la ventana de autenticación
        VentanaAutenticacion(self.root, abrir_inventario)
    # =====================================================================
    # MÉTODOS AUXILIARES Y ACTUALIZACIÓN AUTOMÁTICA DE VISTAS
    # =====================================================================
    def _obtener_id_seleccionado(self) -> int:
        seleccion = self.tabla_pedidos.selection()
        if not seleccion:
            messagebox.showwarning("Selección Obligatoria", "Por favor, seleccione primero un pedido de la lista central.")
            return None
        return int(self.tabla_pedidos.item(seleccion[0], "values")[0])

    def mostrar_detalle_seleccionado(self, event):
        seleccion = self.tabla_pedidos.selection()
        if seleccion:
            pedido_id = int(self.tabla_pedidos.item(seleccion[0], "values")[0])
            self._vistas.refrescar_listbox_detalle(pedido_id)

    def refrescar_listbox_detalle(self, pedido_id):
        self._vistas.refrescar_listbox_detalle(pedido_id)

    def actualizar_tablas(self):
        self._vistas.actualizar_tablas()

    def borrar_aviso(self):
        # Borra las alertas seleccionadas en la tabla de notificaciones (sin confirmación)
        seleccion = ()
        try:
            seleccion = self.tabla_notificaciones.selection()
        except Exception:
            seleccion = ()
        if not seleccion:
            messagebox.showwarning("Seleccionar aviso", "Seleccione al menos un aviso para borrar.")
            return
        for iid in seleccion:
            try:
                alert_id = int(iid)
                if hasattr(self.sistema, 'alertService'):
                    self.sistema.alertService.delete_alert(alert_id)
            except Exception:
                pass
        # refrescar vistas
        self.actualizar_tablas()

    def mostrar_alerta_detalle(self, event):
        # Muestra el mensaje completo de la alerta seleccionada en un diálogo
        sel = ()
        try:
            sel = self.tabla_notificaciones.selection()
        except Exception:
            sel = ()
        if not sel:
            return
        iid = sel[0]
        try:
            alert_id = int(iid)
            alerts = self.sistema.alertService.list_alerts() if hasattr(self.sistema, 'alertService') else []
            alert = next((a for a in alerts if a.get('id')==alert_id), None)
            if alert:
                messagebox.showinfo("Detalle de Aviso", alert.get('mensaje',''))
        except Exception:
            pass

    def resolver_aviso(self):
        # Resuelve las alertas seleccionadas en la tabla de notificaciones
        seleccion = ()
        try:
            seleccion = self.tabla_notificaciones.selection()
        except Exception:
            seleccion = ()
        if not seleccion:
            messagebox.showwarning("Seleccionar aviso", "Seleccione al menos un aviso para resolver.")
            return
        for iid in seleccion:
            try:
                alert_id = int(iid)
                if hasattr(self.sistema, 'alertService'):
                    self.sistema.alertService.delete_alert(alert_id)
            except Exception:
                pass
        # refrescar vistas
        self.actualizar_tablas()