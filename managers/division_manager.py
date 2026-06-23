from services.division_service import DivisionService
from entidades.division import Division
from validadores.validador_service import ValidadorService
from repositorio import cargarPedidos, guardarPedidos

class DivisionManager(DivisionService):
    def __init__(self, validador: ValidadorService):
        self._validador = validador

    def dividirCuenta(self, pedidoId: int, personas: int, tiposPago: list):
        pedidos = cargarPedidos()
        pedido = next((p for p in pedidos if p.id == pedidoId), None)
        
        self._validador.validarPedido(pedido)
        
        if pedido.boleta is None:
            raise ValueError("Primero debe generar la boleta antes de dividir la cuenta.")
        
        # Calcular monto por persona
        total_con_propina = pedido.boleta.total + pedido.boleta.propina
        montoPorPersona = total_con_propina // personas
        
        divisiones = []
        for i in range(personas):
            tipo = tiposPago[i] if i < len(tiposPago) else tiposPago[-1]
            
            # Validación individual de cada cuota
            # Si el monto por persona excede el límite del tipo de pago, lanzará error aquí
            self._validador.validarPago(tipo)
            self._validador.validarLimitePago(tipo, montoPorPersona)
            
            divisiones.append(
                Division(
                    monto=montoPorPersona,
                    tipoPago=tipo
                )
            )
            
        pedido.boleta.divisiones = divisiones
        guardarPedidos(pedidos)
        return divisiones