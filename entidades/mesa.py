# Importamos dataclass para que Python arme la estructura de la mesa automáticamente
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Mesa:
    numero: int         # El número de identificación de la mesa (Mesa 1, Mesa 2, etc.)
    capacidad: int      # Cuántas personas caben sentadas en esta mesa
    ocupada: bool = False  # Dice si la mesa tiene clientes (True) o está vacía (False). Parte vacía por defecto.
    ocupada_desde: Optional[str] = None  # ISO timestamp cuando pasó a estar ocupada

    def cambiarEstado(self):
        """
        INTERRUPTOR DE ESTADO: Funciona como un botón de la luz. 
        Si la mesa estaba libre (False), la cambia a ocupada (True), y viceversa.
        Además registra la hora de ocupación para alertas temporales.
        """
        self.ocupada = not self.ocupada
        if self.ocupada:
            # Guardamos la hora actual en formato ISO
            self.ocupada_desde = datetime.now().isoformat()
        else:
            # Liberando la mesa: borramos el timestamp
            self.ocupada_desde = None

    def to_dict(self):
        """
        CONVERTIR A TEXTO: Transforma los datos de la mesa a un formato simple
        para poder guardarlos dentro del archivo JSON del disco duro.
        """
        return {
            "numero": self.numero,
            "capacidad": self.capacidad,
            "ocupada": self.ocupada,
            "ocupada_desde": self.ocupada_desde
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
            ocupada=d.get("ocupada", False),
            ocupada_desde=d.get("ocupada_desde", None)
        )