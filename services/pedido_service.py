# ABC permite crear servicios base que obligan
# a implementar ciertos métodos en otras clases
from abc import ABC, abstractmethod


# Servicio base para manejar pedidos
class PedidoService(ABC):

    # Método obligatorio para crear pedidos (ahora acepta hasta 2 mesas según la regla)
    @abstractmethod
    def crearPedido(self, cliente: str, numeroMesa1: int, numeroMesa2: int = None):
        pass

    # Método obligatorio para agregar platos
    @abstractmethod
    def agregarPlato(self, pedidoId: int, nombrePlato: str):
        pass

    # Método obligatorio para modificar platos
    @abstractmethod
    def modificarPlato(self, pedidoId: int, indice: int, nombrePlato: str):
        pass

    # Método obligatorio para eliminar platos
    @abstractmethod
    def eliminarPlato(self, pedidoId: int, indice: int):
        pass

    # Método obligatorio para cancelar pedidos
    @abstractmethod
    def cancelarPedido(self, pedidoId: int):
        pass

    # Método obligatorio para agregar notas a platos
    @abstractmethod
    def agregarNotaPlato(self, pedidoId: int, indice: int, nota: str):
        pass

    # Método obligatorio para agregar notas al pedido
    @abstractmethod
    def agregarNotaPedido(self, pedidoId: int, nota: str):
        pass

    # Método obligatorio para ver detalles del pedido
    @abstractmethod
    def verDetalle(self, pedidoId: int):
        pass

    # Método obligatorio para calcular el total
    @abstractmethod
    def calcularTotal(self, pedidoId: int):
        pass