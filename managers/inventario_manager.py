# Importamos el servicio base de inventario
from services.inventario_service import InventarioService
# Servicio encargado de validar datos
from validadores.validador_service import ValidadorService
# Funciones para cargar y guardar datos desde el repositorio
from repositorio import cargarPlatos, guardarPlatos, cargarIngredientes, guardarIngredientes
# Importamos la librería matemática para el redondeo estricto
import math

class InventarioManager(InventarioService):

    def __init__(self, validador: ValidadorService):
        self._validador = validador

    def actualizarStock(self, nombrePlato: str, cantidad: int):
        """
        Descuenta los ingredientes necesarios de la receta del plato.
        Aproxima cualquier cantidad decimal al número entero mayor (ceil)
        y elimina el formato .0 para mantener el inventario en enteros puros.
        """
        platos = cargarPlatos()
        plato = next((p for p in platos if p.nombre == nombrePlato), None)
        
        self._validador.validarPlato(plato)

        # Si el plato no tiene receta establecida, no hay ingredientes que descontar
        if not plato.receta:
            return

        ingredientes_sistema = cargarIngredientes()

        # Recorremos la receta del plato para descontar o devolver cada insumo
        for item in plato.receta:
            nom_ing = item["ingrediente"]
            cant_receta = item["cantidad"]

            # Buscamos el ingrediente en el maestro de inventario
            ing = next((i for i in ingredientes_sistema if i.nombre == nom_ing), None)
            if ing:
                # 1. Calculamos el uso bruto (ej: 1.5 * 1 = 1.5)
                uso_bruto = cant_receta * cantidad
                
                # 2. REGLA DE ORO: Si es positivo (descuento), aplicamos ceil para aproximar al mayor (1.5 -> 2)
                # Si es negativo (devolución), usamos floor para mantener la proporción simétrica.
                if uso_bruto > 0:
                    descuento_total = int(math.ceil(uso_bruto))
                else:
                    descuento_total = int(math.floor(uso_bruto))

                # 3. Forzamos que el stock actual sea leído como entero puro (elimina el .0)
                stock_actual = int(ing.stock_unidades)

                # 4. Resta o suma atómica entre enteros puros
                ing.stock_unidades = max(0, stock_actual - descuento_total)

        # Guardamos los ingredientes actualizados en ingredientes.json como enteros
        guardarIngredientes(ingredientes_sistema)

    def marcarNoDisponible(self, nombrePlato: str):
        """Desactiva temporalmente un plato de forma manual"""
        platos = cargarPlatos()
        plato = next((p for p in platos if p.nombre == nombrePlato), None)
        
        self._validador.validarPlato(plato)
        
        plato.disponible = False
        guardarPlatos(platos)
    def ajustarStockIngredienteManual(self, nombreIngrediente: str, nuevo_valor: int):
        """
        Sobrescribe el stock de un ingrediente de forma directa en ingredientes.json.
        """
        ingredientes_sistema = cargarIngredientes()
        ing = next((i for i in ingredientes_sistema if i.nombre == nombreIngrediente), None)
        
        if ing:
            # Asignación directa del valor manual
            ing.stock_unidades = nuevo_valor
            
            # Guardamos los ingredientes actualizados
            guardarIngredientes(ingredientes_sistema)
        else:
            raise Exception(f"Ingrediente '{nombreIngrediente}' no encontrado en el sistema.")