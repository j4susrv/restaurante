from dataclasses import dataclass
from typing import Optional

@dataclass
class Alerta:
    id: int
    tipo: str
    mensaje: str
    referencia: str
    created_at: str
    estado: str = 'activo'
    resolved_at: Optional[str] = None
