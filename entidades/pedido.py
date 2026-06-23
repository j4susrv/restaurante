# Herramientas para crear clases y listas automáticamente
from dataclasses import dataclass, field
# Sirve para trabajar con listas y datos opcionales
from typing import List, Optional
# Importamos las clases necesarias para el pedido
from entidades.plato import Plato
from entidades.mesa import Mesa
from entidades.boleta import Boleta

# Representa un pedido dentro del restaurante
@dataclass
class Pedido:

    # Datos principales del pedido
    id: int
    cliente: str

    # Ahora manejamos un máximo de 2 mesas por pedido para cumplir la regla
    mesa1: Mesa
    mesa2: Optional[Mesa] = None

    # Lista de platos del pedido
    # Cada pedido tendrá su propia lista independiente
    platos: List[Plato] = field(default_factory=list)

    # Estado y nota del pedido
    estado: str = "abierto"
    nota: str = ""

    # Boleta asociada al pedido (si existe)
    boleta: Optional[Boleta] = None
    created_at: str = ""

    # Agrega un plato a la lista del pedido
    def agregarPlato(self, plato: Plato):
        self.platos.append(plato)
        
    # Convierte el pedido a diccionario
    # para poder guardarlo en JSON
    def to_dict(self):
        return {
            "id": self.id,
            "cliente": self.cliente,
            # Convierte la mesa 1 y la mesa 2 (si existe) a diccionario
            "mesa1": self.mesa1.to_dict(),
            "mesa2": self.mesa2.to_dict() if self.mesa2 else None,
            # Convierte cada plato de la lista
            "platos": [p.to_dict() for p in self.platos],

            "estado": self.estado,
            "nota": self.nota,
            "fechaCreacion": self.created_at,
            # Si existe boleta la convierte,
            # si no deja None
            "boleta": self.boleta.to_dict() if self.boleta else None
        }

    # Reconstruye un pedido usando datos del JSON
    @staticmethod
    def from_dict(d):
        return Pedido(
            id=d["id"],
            cliente=d["cliente"],
            # Reconstruye la mesa 1 y la mesa 2 de manera segura
            mesa1=Mesa.from_dict(d["mesa1"]),
            mesa2=Mesa.from_dict(d["mesa2"]) if d.get("mesa2") else None,
            # Reconstruye la lista de platos
            platos=[Plato.from_dict(p) for p in d.get("platos", [])],
            # Si no encuentra datos, usa valores por defecto
            estado=d.get("estado", "abierto"),
            nota=d.get("nota", ""),
            # Reconstruye la boleta si existe
            boleta=Boleta.from_dict(d["boleta"]) if d.get("boleta") else None,
            created_at=d.get("fechaCreacion", "")
        )