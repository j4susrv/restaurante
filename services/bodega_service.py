# services/bodega_service.py
from abc import ABC, abstractmethod

class BodegaService(ABC):
    
    @abstractmethod
    def listarMateriasPrimas(self) -> list:
        """Contrato obligatorio para recuperar el stock crudo de ingredientes."""
        pass