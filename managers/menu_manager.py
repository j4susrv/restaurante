from services.menu_service import MenuService
from repositorio import cargarPlatos

class MenuManager(MenuService):
    #Se van a listar los platos disponibles
    def listarPlatosDisponibles(self):
        #se van a cargar todo los platos y si el stock es suficinete osea mayor a 0 entonces se van a listar.
        return [p for p in cargarPlatos() if p.disponible and p.stock > 0]