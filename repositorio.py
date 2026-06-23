# Permite trabajar con archivos JSON
import json
# Permite verificar si existen archivos
import os
# Clases principales del sistema
from entidades.pedido import Pedido
from entidades.plato import Plato
from entidades.mesa import Mesa
from entidades.ingrediente import Ingrediente

# Archivos JSON usados para guardar la información
PLATOS_FILE = "platos.json"
MESAS_FILE = "mesas.json"
PEDIDOS_FILE = "pedidos.json"
INGREDIENTES_FILE = "ingredientes.json"

# Carga todos los platos desde el JSON
def cargarPlatos() -> list:

    # Si el archivo no existe, retorna lista vacía
    if not os.path.exists(PLATOS_FILE):
        return []

    try:
        with open(PLATOS_FILE, "r", encoding="utf-8") as f:

            # Lee los datos del JSON
            datos = json.load(f)

            # Reconstruye cada plato
            return [Plato.from_dict(p) for p in datos]

    # Si ocurre un error, retorna lista vacía
    except (json.JSONDecodeError, KeyError):
        return []
# Guarda los platos en el JSON
def guardarPlatos(platos: list):

    with open(PLATOS_FILE, "w", encoding="utf-8") as f:

        # Convierte cada plato a diccionario
        datos = [p.to_dict() for p in platos]

        # Guarda los datos en formato JSON
        json.dump(datos, f, ensure_ascii=False, indent=4)

# Carga todas las mesas desde el JSON
def cargarMesas() -> list:

    if not os.path.exists(MESAS_FILE):
        return []

    try:
        with open(MESAS_FILE, "r", encoding="utf-8") as f:

            datos = json.load(f)

            # Reconstruye cada mesa
            return [Mesa.from_dict(m) for m in datos]

    except (json.JSONDecodeError, KeyError):
        return []


# Guarda las mesas en el JSON
def guardarMesas(mesas: list):

    with open(MESAS_FILE, "w", encoding="utf-8") as f:

        # Convierte cada mesa a diccionario
        datos = [m.to_dict() for m in mesas]

        json.dump(datos, f, ensure_ascii=False, indent=4)

# Carga todos los pedidos desde el JSON
def cargarPedidos() -> list:

    if not os.path.exists(PEDIDOS_FILE):
        return []
    try:
        with open(PEDIDOS_FILE, "r", encoding="utf-8") as f:

            datos = json.load(f)

            # Reconstruye cada pedido
            return [Pedido.from_dict(p) for p in datos]

    except (json.JSONDecodeError, KeyError):
        return []

# Guarda los pedidos en el JSON
from datetime import date

def guardarPedidos(pedidos: list):

    # Asegurarse que cada pedido tenga fecha de creación antes de guardar
    for p in pedidos:
        if not getattr(p, 'created_at', None):
            p.created_at = date.today().strftime("%d/%m/%Y")

    with open(PEDIDOS_FILE, "w", encoding="utf-8") as f:

        # Convierte cada pedido a diccionario
        datos = [p.to_dict() for p in pedidos]

        json.dump(datos, f, ensure_ascii=False, indent=4)

# Carga todos los ingredientes desde el JSON
def cargarIngredientes() -> list:

    if not os.path.exists(INGREDIENTES_FILE):
        return []

    try:
        with open(INGREDIENTES_FILE, "r", encoding="utf-8") as f:

            datos = json.load(f)

            # Reconstruye cada ingrediente
            return [Ingrediente.from_dict(i) for i in datos]

    except (json.JSONDecodeError, KeyError):
        return []

# Guarda los ingredientes en el JSON
def guardarIngredientes(ingredientes: list):

    with open(INGREDIENTES_FILE, "w", encoding="utf-8") as f:

        # Convierte cada ingrediente a diccionario
        datos = [i.to_dict() for i in ingredientes]

        json.dump(datos, f, ensure_ascii=False, indent=4)