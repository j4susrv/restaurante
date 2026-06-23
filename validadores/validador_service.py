# Clases principales usadas en las validaciones
from entidades.pedido import Pedido
from entidades.plato import Plato
from entidades.mesa import Mesa

# Importamos los validadores especializados
from .validador_pedido import ValidadorPedido
from .validador_pago import ValidadorPago
from .validador_plato import ValidadorPlato
from .validador_mesa import ValidadorMesa

# Servicio central encargado de todas las validaciones
class ValidadorService:

    def __init__(self):

        # Creamos cada validador especializado
        self._validadorPedido = ValidadorPedido()
        self._validadorPago = ValidadorPago()
        self._validadorPlato = ValidadorPlato()
        self._validadorMesa = ValidadorMesa()


    # Valida pedidos según el tipo de validación necesaria
    def validarPedido(self, pedido: Pedido, abierto=False, cancelacion=False):

        # Validación para cancelación
        if cancelacion:
            self._validadorPedido.validarCancelacion(pedido)

        # Validación para pedidos abiertos
        elif abierto:
            self._validadorPedido.validarPedidoAbierto(pedido)

        # Validación normal
        else:
            self._validadorPedido.validarPedido(pedido)

    # Valida el nombre del cliente
    def validarCliente(self, cliente: str):
        self._validadorPedido.validarCliente(cliente)


    def validarNota(self, nota: str, campo: str = "Nota"):
        self._validadorPedido.validarNota(nota, campo)

    def validarIndice(self, indice: int, lista: list, tipo: str = "elemento"):
        self._validadorPlato.validarIndice(indice, lista, tipo)

    # Valida tipos de pago
    def validarPago(self, tipoPago: str):
        self._validadorPago.validarTipoPago(tipoPago)

    # Valida montos de propina
    """def validarPropina(self, monto_propina,tipo_pago,monto_subtotal):
        self._validadorPago.validarPropina(monto_propina,tipo_pago,monto_subtotal)"""

    # Valida límites por método de pago (tarjeta/transferencia/efectivo)
    def validarLimitePago(self, tipoPago: str, monto: int):
        self._validadorPago.validarLimitePago(tipoPago, monto)

    # Valida platos, stock y disponibilidad
    def validarPlato(self, plato: Plato, checkStock=False, checkDisponibilidad=False):
        self._validadorPlato.validarPlato(plato, checkStock, checkDisponibilidad)

    # Valida que la mesa exista
    def validarMesa(self, mesa: Mesa):
        self._validadorMesa.validarMesa(mesa)
    
    # Dentro de tu ValidadorService agregas el puente:

    def validarMesasNoRepetidas(self, mesa1: Mesa, mesa2: Mesa):
        # Llama al validador experto en mesas
        self._validadorMesa.validarMesasNoRepetidas(mesa1, mesa2)

    # Valida capacidad de personas en una mesa
    def validarCapacidad(self, mesa: Mesa, personas: int):
        self._validadorMesa.validarCapacidad(mesa, personas)