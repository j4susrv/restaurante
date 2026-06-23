# Clase Plato
from entidades.plato import Plato

# Clase encargada de validar platos
class ValidadorPlato:

    def validarPlato(self, plato: Plato, checkStock=False, checkDisponibilidad=False):
        """
        Verifica que el plato exista y opcionalmente
        revisa el stock calculado y su disponibilidad.
        """
        # Verifica que el plato exista
        if plato is None:
            raise ValueError("El plato seleccionado no existe en el menú.")

        # Verifica si el plato está disponible manualmente
        if checkDisponibilidad and not plato.disponible:
            raise ValueError(f"El plato '{plato.nombre}' no está disponible temporalmente.")

        # Verifica si queda stock dinámico de ingredientes
        if checkStock and plato.stock <= 0:
            raise ValueError(f"No queda stock disponible de ingredientes para preparar '{plato.nombre}'.")

    def validarPrecio(self, precio: int):
        """Verifica que el precio sea válido"""
        if precio <= 0:
            raise ValueError("El precio del plato debe ser mayor a cero.")

    def validarIndice(self, indice: int, lista: list, tipo: str = "elemento"):
        """Verifica que el índice exista dentro de una lista (como la lista de consumos)"""
        if indice < 0 or indice >= len(lista):
            raise IndexError(f"El índice {indice} de {tipo} no es válido en la lista.")