import math
from dataclasses import dataclass

@dataclass
class Ingrediente:
    nombre: str
    precio_unidad: int
    stock_unidades: int
    subcategoria: str

    def to_dict(self) -> dict:
        return {
            "nombre": self.nombre,
            "precio_unidad": int(self.precio_unidad),
            "stock_unidades": int(self.stock_unidades),  # Asegura enteros al guardar
            "subcategoria": self.subcategoria
        }

    @staticmethod
    def from_dict(d: dict):
        # 1. Leemos el stock. Si viene como float (ej: 50.0) o string ("50"), 
        # lo pasamos a float y aplicamos ceil para aproximar al entero mayor.
        stock_original = d.get("stock_unidades", 0)
        stock_limpio = int(math.ceil(float(stock_original)))
        
        # 2. Hacemos lo mismo con el precio por consistencia de tipos numéricos
        precio_limpio = int(math.ceil(float(d.get("precio_unitario", d.get("precio_unidad", 0)))))

        return Ingrediente(
            nombre=d["nombre"],
            precio_unidad=precio_limpio,
            stock_unidades=stock_limpio,  # <-- ENTERO PURO Y REDONDEADO GARANTIZADO
            subcategoria=d["subcategoria"]
        )