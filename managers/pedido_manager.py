# Permite copiar objetos sin modificar el original
import copy
from datetime import date
# Servicio base de pedidos
from services.pedido_service import PedidoService
# Servicio de inventario
from services.inventario_service import InventarioService
# Clase Pedido
from entidades.pedido import Pedido
# Servicio encargado de validaciones
from validadores.validador_service import ValidadorService
# Clase auxiliar que calcula totales
from pedido_calculator import PedidoCalculator
# Funciones para cargar y guardar datos
from repositorio import (
    cargarPedidos, guardarPedidos,
    cargarPlatos, cargarMesas, guardarMesas
)
# Manager encargado de manejar pedidos
class PedidoManager(PedidoService):

    # Recibe el validador y el servicio de inventario
    def __init__(self, validador: ValidadorService, inventarioService: InventarioService):
        self._validador = validador
        self._calculator = PedidoCalculator()
        self._inventarioService = inventarioService

    # Genera automáticamente el siguiente ID
    def _siguienteId(self, pedidos: list) -> int:
        return max((p.id for p in pedidos), default=0) + 1

    # Crea un nuevo pedido
    def crearPedido(self, cliente: str, numeros_mesas: list):
        # Verifica el nombre del cliente
        self._validador.validarCliente(cliente)
        # Verifica que haya al menos una mesa
        if not numeros_mesas:
            raise ValueError("Debe seleccionar al menos una mesa para abrir el pedido.")
        # Máximo permitido: 2 mesas
        if len(numeros_mesas) > 2:
            raise ValueError("No se pueden seleccionar más de 2 mesas para un mismo pedido.")
        # Carga las mesas guardadas
        mesas_totales = cargarMesas()
        mesas_seleccionadas = []
        # Busca y valida cada mesa
        for num in numeros_mesas:
            mesa = next((m for m in mesas_totales if m.numero == num), None)
            self._validador.validarMesa(mesa)
            # Verifica que la mesa no esté ocupada
            if mesa.ocupada:
                raise ValueError(f"La mesa {num} ya está ocupada por otro servicio.")
            mesas_seleccionadas.append(mesa)
            
        # NUEVA VALIDACIÓN: Si eligió dos mesas, verificamos que no sea la misma repetida
        if len(mesas_seleccionadas) == 2:
            self._validador.validarMesasNoRepetidas(mesas_seleccionadas[0], mesas_seleccionadas[1])

        # Marca las mesas como ocupadas
        for mesa in mesas_seleccionadas:
            mesa.cambiarEstado()
        guardarMesas(mesas_totales)
        # Carga los pedidos existentes
        pedidos = cargarPedidos()
        
        # SOLUCIÓN: Creamos el pedido usando la lista nativa de forma segura
        pedido = Pedido(
            id=self._siguienteId(pedidos),
            cliente=cliente.strip(),
            mesa1=mesas_seleccionadas[0],
            mesa2=mesas_seleccionadas[1] if len(mesas_seleccionadas) > 1 else None,
            created_at=date.today().strftime("%d/%m/%Y")
        )
        
        # Guarda el pedido
        pedidos.append(pedido)
        guardarPedidos(pedidos)
        return pedido

    # Agrega un plato al pedido
    def agregarPlato(self, pedidoId: int, nombrePlato: str):
        pedidos = cargarPedidos()
        # Busca el pedido
        pedido = next((p for p in pedidos if p.id == pedidoId), None)
        # Verifica que exista y esté abierto
        self._validador.validarPedido(pedido, abierto=True)
        platos = cargarPlatos()
        # Busca el plato
        plato = next((p for p in platos if p.nombre == nombrePlato), None)
        # Verifica stock y disponibilidad
        self._validador.validarPlato(
            plato,
            checkStock=True,
            checkDisponibilidad=True
        )
        # Agrega una copia del plato al pedido
        pedido.agregarPlato(copy.deepcopy(plato))
        guardarPedidos(pedidos)
        # Descuenta stock del inventario
        self._inventarioService.actualizarStock(nombrePlato, 1)
        return pedido

    # Modifica un plato del pedido
    def modificarPlato(self, pedidoId: int, indice: int, nombrePlato: str):
        pedidos = cargarPedidos()
        pedido = next((p for p in pedidos if p.id == pedidoId), None)
        self._validador.validarPedido(pedido, abierto=True)
        # Verifica que el índice exista
        self._validador.validarIndice(indice, pedido.platos, "plato")
        platos = cargarPlatos()
        # Busca el nuevo plato
        nuevo = next((p for p in platos if p.nombre == nombrePlato), None)
        self._validador.validarPlato(
            nuevo,
            checkStock=True,
            checkDisponibilidad=True
        )
        # Devuelve el stock del plato anterior
        nombreAnterior = pedido.platos[indice].nombre
        self._inventarioService.actualizarStock(nombreAnterior, -1)
        # Reemplaza el plato
        pedido.platos[indice] = copy.deepcopy(nuevo)
        guardarPedidos(pedidos)
        # Descuenta stock del nuevo plato
        self._inventarioService.actualizarStock(nombrePlato, 1)
        return pedido

    # Elimina un plato del pedido
    def eliminarPlato(self, pedidoId: int, indice: int):
        pedidos = cargarPedidos()
        pedido = next((p for p in pedidos if p.id == pedidoId), None)
        self._validador.validarPedido(pedido, abierto=True)
        self._validador.validarIndice(indice, pedido.platos, "plato")
        # Guarda el nombre del plato eliminado
        nombre = pedido.platos[indice].nombre
        # Elimina el plato
        del pedido.platos[indice]
        guardarPedidos(pedidos)
        # Devuelve el stock al inventario
        self._inventarioService.actualizarStock(nombre, -1)
        return pedido

    # Cancela un pedido
    def cancelarPedido(self, pedidoId: int):
        pedidos = cargarPedidos()
        pedido = next((p for p in pedidos if p.id == pedidoId), None)
        self._validador.validarPedido(pedido, cancelacion=True)
        # Devuelve el stock de todos los platos
        for plato in pedido.platos:
            self._inventarioService.actualizarStock(plato.nombre, -1)
        # Cambia el estado del pedido
        pedido.estado = "cancelado"
        # Vacía la lista de platos
        pedido.platos = []
        mesas = cargarMesas()
        
        # Busca y libera la mesa 1
        mesa1 = next((m for m in mesas if m.numero == pedido.mesa1.numero), None)
        if mesa1 and mesa1.ocupada:
            mesa1.cambiarEstado()
            
        # Busca y libera la mesa 2 si existía
        if pedido.mesa2:
            mesa2 = next((m for m in mesas if m.numero == pedido.mesa2.numero), None)
            if mesa2 and mesa2.ocupada:
                mesa2.cambiarEstado()
                
        guardarMesas(mesas)
        guardarPedidos(pedidos)
        return pedido

    # Agrega una nota a un plato
    def agregarNotaPlato(self, pedidoId: int, indice: int, nota: str):
        self._validador.validarNota(nota, "Nota del plato")
        pedidos = cargarPedidos()
        pedido = next((p for p in pedidos if p.id == pedidoId), None)
        self._validador.validarPedido(pedido, abierto=True)
        self._validador.validarIndice(indice, pedido.platos, "plato")
        # Guarda la nota
        pedido.platos[indice].nota = nota.strip()
        guardarPedidos(pedidos)
        return pedido
        
    # Agrega una nota general al pedido
    def agregarNotaPedido(self, pedidoId: int, nota: str):
        self._validador.validarNota(nota, "Nota del pedido")
        pedidos = cargarPedidos()
        pedido = next((p for p in pedidos if p.id == pedidoId), None)
        self._validador.validarPedido(pedido, abierto=True)
        # Guarda la nota
        pedido.nota = nota.strip()
        guardarPedidos(pedidos)
        return pedido

    # Muestra el detalle del pedido
    def verDetalle(self, pedidoId: int):
        pedidos = cargarPedidos()
        pedido = next((p for p in pedidos if p.id == pedidoId), None)
        self._validador.validarPedido(pedido)
        return pedido
        
    # Calcula el total del pedido
    def calcularTotal(self, pedidoId: int) -> int:
        pedidos = cargarPedidos()
        pedido = next((p for p in pedidos if p.id == pedidoId), None)
        self._validador.validarPedido(pedido)
        return self._calculator.calcularTotal(pedido)