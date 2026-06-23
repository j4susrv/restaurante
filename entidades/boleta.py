from dataclasses import dataclass, field
from typing import List
from entidades.division import Division
from utils_format import formato_moneda

# Usamos @dataclass para que Python arme la estructura de la boleta automáticamente
@dataclass
class Boleta:
    total: int                  # La cuenta total de lo que se comió (el subtotal)
    tipoPago: str               # Cómo pagó el cliente (efectivo, tarjeta, etc.)
    propina: int = 0            # La propina del mesero (empieza en 0 si no ponen nada)
    
    # Guarda la lista de los amigos que pagaron por separado.
    # El "field" evita que las cuentas de diferentes mesas se mezclen entre sí.
    divisiones: List[Division] = field(default_factory=list)

    def mostrar(self) -> str:
        """
        Este método fabrica el texto de la boleta para que parezca un ticket real.
        """
        lineas = [
            "===== BOLETA =====",
            f"Subtotal:   ${formato_moneda(self.total)}",
            f"Propina:    ${formato_moneda(self.propina)}",
            f"TOTAL:      ${formato_moneda(self.total + self.propina)}", # Suma la cuenta más la propina
            f"Pago:       {self.tipoPago}",
        ]
        
        # Si los amigos pidieron dividir la cuenta, se activa este bloque:
        if self.divisiones:
            lineas.append("--- División de cuenta ---")
            # Cuenta a las personas (Persona 1, Persona 2...) y muestra cuánto pagó cada una
            for i, d in enumerate(self.divisiones, 1):
                lineas.append(f"   Persona {i}: ${formato_moneda(d.monto)}  ({d.tipoPago})")
                
        # Junta todas las líneas anteriores con un salto de línea para armar el ticket final
        return "\n".join(lineas)

    def to_dict(self):
        """
        CONVERTIR A TEXTO: Desarma la boleta y la convierte en un formato simple
        para que se pueda guardar dentro del archivo JSON del disco duro.
        """
        return {
            "total": self.total,
            "tipoPago": self.tipoPago,
            "propina": self.propina,
            # Desarma también la lista de los amigos que pagaron por separado
            "divisiones": [d.to_dict() for d in self.divisiones]
        }

    @staticmethod
    def from_dict(d):
        """
        RECONSTRUIR BOLETA: Toma los datos guardados en el archivo JSON
        y vuelve a armar la boleta con todas sus funciones activas.
        """
        return Boleta(
            total=d["total"],
            tipoPago=d["tipoPago"],
            propina=d.get("propina", 0), # Si la boleta es vieja y no tiene propina, le pone 0
            # Vuelve a armar la lista de amigos que pagaron por separado
            divisiones=[Division.from_dict(x) for x in d.get("divisiones", [])]
        )