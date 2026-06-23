from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Plato:
    nombre: str
    receta: List[Dict] = field(default_factory=list) # Formato: [{"ingrediente": "Tomate", "cantidad": 2}]
    margen_ganancia: float = 1.5                    # Multiplicador del costo base (ej: costo * 1.5)
    disponible: bool = True
    nota: str = ""

    @property
    def precio(self) -> int:
        """Calcula el precio dinámicamente sumando el costo de los ingredientes * margen"""
        if not self.receta:
            return 0
        
        import repositorio
        ingredientes_sistema = repositorio.cargarIngredientes()
        costo_total = 0
        
        for item in self.receta:
            nom_ing = item["ingrediente"]
            cant = item["cantidad"]
            
            ing = next((i for i in ingredientes_sistema if i.nombre == nom_ing), None)
            if ing:
                costo_total += ing.precio_unidad * cant
                
        return int(costo_total * self.margen_ganancia)

    @property
    def stock(self) -> int:
        """Calcula el stock basándose en el ingrediente que tenga menos raciones disponibles"""
        if not self.receta:
            return 0
        
        import repositorio
        ingredientes_sistema = repositorio.cargarIngredientes()
        posibles_stocks = []
        
        for item in self.receta:
            nom_ing = item["ingrediente"]
            cant_necesaria = item["cantidad"]
            
            ing = next((i for i in ingredientes_sistema if i.nombre == nom_ing), None)
            if ing:
                platos_posibles = ing.stock_unidades // cant_necesaria
                posibles_stocks.append(platos_posibles)
            else:
                posibles_stocks.append(0)
                
        return min(posibles_stocks) if posibles_stocks else 0

    def to_dict(self) -> dict:
        return {
            "nombre": self.nombre,
            "receta": self.receta,
            "margen_ganancia": self.margen_ganancia,
            "disponible": self.disponible,
            "nota": self.nota
        }

    @staticmethod
    def from_dict(d: dict):
        return Plato(
            nombre=d["nombre"],
            receta=d.get("receta", []),
            margen_ganancia=d.get("margen_ganancia", 1.5),
            disponible=d.get("disponible", True),
            nota=d.get("nota", "")
        )