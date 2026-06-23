# ABC permite crear servicios base que obligan
# a implementar ciertos métodos en otras clases
from abc import ABC, abstractmethod
# Servicio base para la división de cuentas
class DivisionService(ABC):
    # Método obligatorio que deberá implementar el manager
    @abstractmethod
    def dividirCuenta(self, pedidoId: int, personas: int, tiposPago: list):
        pass