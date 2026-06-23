# Servicio central de validaciones
from validadores.validador_service import ValidadorService

# Managers principales del sistema
from managers.pedido_manager import PedidoManager
from managers.factura_manager import FacturaManager
from managers.inventario_manager import InventarioManager
from managers.division_manager import DivisionManager
from managers.menu_manager import MenuManager
from managers.bodega_manager import BodegaManager

# Clase principal que conecta todo el sistema
class Restaurante:

    # Inicializa todos los servicios y managers
    def __init__(self):

        # Servicio encargado de todas las validaciones
        self.validador_service = ValidadorService()

        # Manager del inventario
        self.inventarioService = InventarioManager(self.validador_service)

        # Manager de pedidos
        # También usa inventario para actualizar stock
        self.pedidoService = PedidoManager(
            self.validador_service,
            self.inventarioService
        )

        # Manager de división de cuentas
        self.divisionService = DivisionManager(self.validador_service)

        # Manager de facturas y boletas
        self.facturaService = FacturaManager(
            self.validador_service,
            self.divisionService
        )

        # Manager del menú
        self.menuService = MenuManager()
        self.bodegaService = BodegaManager(self.validador_service)

    # Retorna el validador central
    def obtener_validador(self) -> ValidadorService:
        return self.validador_service