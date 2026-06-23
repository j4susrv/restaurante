# managers/bodega_manager.py
from services.bodega_service import BodegaService
from validadores.validador_service import ValidadorService
import repositorio

class BodegaManager(BodegaService):
    
    def __init__(self, validador: ValidadorService):
        self._validador = validador

    def listarMateriasPrimas(self) -> list:
        # El manager pide los datos al repositorio de manera desacoplada
        return repositorio.cargarIngredientes()