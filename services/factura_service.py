# ABC permite crear servicios base que obligan
# a implementar ciertos métodos en otras clases
from abc import ABC, abstractmethod

# Servicio base para manejar boletas y propinas
class FacturaService(ABC):

    # Método obligatorio para generar una boleta
    @abstractmethod
    def generarBoleta(self, pedidoId: int, tipoPago: str,monto_propina: int):
        pass
