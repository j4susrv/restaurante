# Importamos el servicio base de inventario
from services.inventario_service import InventarioService
# Servicio encargado de validar datos
from validadores.validador_service import ValidadorService
# Funciones para cargar y guardar datos desde el repositorio
from repositorio import cargarPlatos, guardarPlatos, cargarIngredientes, guardarIngredientes
# Importamos la librería matemática para el redondeo estricto
import math

class InventarioManager(InventarioService):

    def __init__(self, validador: ValidadorService, alert_service=None):
        self._validador = validador
        self._alert_service = alert_service

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

        # Mantener lista de ingredientes modificados para notificar alertas
        modificados = []

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
                modificados.append(ing)

        # Guardamos los ingredientes actualizados en ingredientes.json como enteros
        guardarIngredientes(ingredientes_sistema)

        # Notificar al servicio de alertas sobre cambios de stock (si existe)
        if self._alert_service:
            for ing in modificados:
                try:
                    self._alert_service.check_stock_for_ingredient(ing)
                except Exception:
                    # No romper la lógica de inventario por fallas en alertas
                    pass

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

            # Notificar al servicio de alertas sobre el cambio
            if self._alert_service:
                try:
                    self._alert_service.check_stock_for_ingredient(ing)
                except Exception:
                    pass
        else:
            raise Exception(f"Ingrediente '{nombreIngrediente}' no encontrado en el sistema.")