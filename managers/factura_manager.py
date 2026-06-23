from services.factura_service import FacturaService
from services.division_service import DivisionService
from entidades.boleta import Boleta
from validadores.validador_service import ValidadorService
from repositorio import cargarPedidos, guardarPedidos, cargarMesas, guardarMesas

class FacturaManager(FacturaService):
    def __init__(self, validador: ValidadorService, divisionService: DivisionService):
        self._validador = validador
        self._divisionService = divisionService

    def generarBoleta(self, pedidoId: int, tipoPago: str, monto_propina: int, dividir: bool = False):
        self._validador.validarPago(tipoPago)
        pedidos = cargarPedidos()
        pedido = next((p for p in pedidos if p.id == pedidoId), None)

        self._validador.validarPedido(pedido, abierto=True)
        if not pedido.platos:
            raise ValueError("No se puede generar boleta de un pedido sin platos.")

        subtotal = sum(p.precio for p in pedido.platos)
        total_final = subtotal + monto_propina

        # Si NO se va a dividir, validamos el total completo ahora mismo
        if not dividir:
            self._validador.validarLimitePago(tipoPago, total_final)

        # Crear y asignar boleta
        pedido.boleta = Boleta(total=subtotal, tipoPago=tipoPago, propina=monto_propina)
        pedido.estado = "cerrado"

        # Liberar mesas
        mesas = cargarMesas()
        for m_num in [pedido.mesa1.numero, pedido.mesa2.numero if pedido.mesa2 else None]:
            if m_num:
                mesa = next((m for m in mesas if m.numero == m_num), None)
                if mesa: mesa.cambiarEstado()
        
        guardarMesas(mesas)
        guardarPedidos(pedidos)
        return pedido.boleta