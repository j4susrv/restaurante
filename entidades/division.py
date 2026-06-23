# Importamos dataclass para ahorrarnos escribir el constructor (__init__) a mano
from dataclasses import dataclass

@dataclass
class Division:
    monto: int      # Guarda la parte del dinero que le toca pagar a esta persona
    tipoPago: str   # Registra cómo pagó esta persona (efectivo, tarjeta, etc.)

    def to_dict(self):
        #convierte a diccionario, transforma este objeto a un texto plano para que el repositorio lo guarde en archivo JSON
        return {
            "monto": self.monto,
            "tipoPago": self.tipoPago
        }

    @staticmethod
    def from_dict(d):
        #convierte a objeto, toma todos los datos guardados en el json y los vuelve a transformar en un objeto Division
        return Division(
            monto=d["monto"],
            tipoPago=d["tipoPago"]
        )
    