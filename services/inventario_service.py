# ABC permite crear servicios base que obligan
# a implementar ciertos métodos en otras clases
from abc import ABC, abstractmethod


# Servicio base para manejar el inventario
class InventarioService(ABC):

    # Método obligatorio para actualizar stock
    @abstractmethod
    def actualizarStock(self, nombrePlato: str, cantidad: int):
        pass

    # Método obligatorio para marcar platos no disponibles
    @abstractmethod
    def marcarNoDisponible(self, nombrePlato: str):
        pass
    @abstractmethod
    def ajustarStockIngredienteManual(self, nombreIngrediente: str, nuevo_valor: int):
        pass