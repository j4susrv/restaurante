# ABC permite crear servicios base que obligan
# a implementar ciertos métodos en otras clases
from abc import ABC, abstractmethod
# Servicio base para manejar el menú
class MenuService(ABC):

    # Método obligatorio para mostrar platos disponibles
    @abstractmethod
    def listarPlatosDisponibles(self):
        pass