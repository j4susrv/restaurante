# Importamos dataclass para que Python arme la estructura de la mesa automáticamente
from dataclasses import dataclass

@dataclass
class Mesa:
    numero: int         # El número de identificación de la mesa (Mesa 1, Mesa 2, etc.)
    capacidad: int      # Cuántas personas caben sentadas en esta mesa
    ocupada: bool = False  # Dice si la mesa tiene clientes (True) o está vacía (False). Parte vacía por defecto.

    def cambiarEstado(self):
        """
        INTERRUPTOR DE ESTADO: Funciona como un botón de la luz. 
        Si la mesa estaba libre (False), la cambia a ocupada (True), y viceversa.
        """
        self.ocupada = not self.ocupada

    def to_dict(self):
        """
        CONVERTIR A TEXTO: Transforma los datos de la mesa a un formato simple
        para poder guardarlos dentro del archivo JSON del disco duro.
        """
        return {
            "numero": self.numero,
            "capacidad": self.capacidad,
            "ocupada": self.ocupada
        }

    @staticmethod
    def from_dict(d):
        """
        RECONSTRUIR MESA: Toma los datos de la mesa guardados en el diccionario ("d") 
        del archivo JSON y los vuelve a cargar como una mesa real en el programa.
        """
        return Mesa(
            numero=d["numero"],
            capacidad=d["capacidad"],
            ocupada=d["ocupada"]
        )