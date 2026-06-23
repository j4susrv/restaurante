# Clase Pedido
from entidades.pedido import Pedido

# Clase auxiliar encargada de calcular totales
class PedidoCalculator:

    # Calcula el total sumando los precios de todos los platos
    def calcularTotal(self, pedido: Pedido) -> int:

        # Si no existe pedido o no tiene platos,
        # retorna 0
        if not pedido or not pedido.platos:
            return 0

        # Suma el precio de cada plato del pedido
        return sum(plato.precio for plato in pedido.platos)