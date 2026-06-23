from entidades.mesa import Mesa

class ValidadorMesa:
    
    def validarMesa(self, mesa: Mesa):
        if mesa is None:
            raise ValueError("La mesa seleccionada no existe en el restaurante.")

    def validarCapacidad(self, mesa: Mesa, personas: int):
        # Este método se mantiene por compatibilidad si se evalúa una sola mesa
        self.validarMesa(mesa)
        if personas <= 0:
            raise ValueError("La cantidad de personas debe ser por lo menos 1.")
        if personas > mesa.capacidad:
            raise ValueError(f"La mesa {mesa.numero} solo tiene capacidad para {mesa.capacidad} personas (ingresaron {personas}).")

    def validarCapacidadTotal(self, capacidad_total: int, personas: int):
        """Valida que el grupo de personas que va a pagar quepa en la capacidad total asignada."""
        if personas <= 0:
            raise ValueError("La cantidad de personas para el pago debe ser por lo menos 1.")
        if personas > capacidad_total:
            raise ValueError(f"El total de pagadores ({personas}) supera la capacidad total del espacio asignado ({capacidad_total}).")

    def validarMaximoMesas(self, cantidad_mesas: int):
        """Asegura que un pedido no supere el límite de 2 mesas entrelazadas."""
        if cantidad_mesas > 2:
            raise ValueError("Por políticas del restaurante, un cliente solo puede reservar un máximo de 2 mesas juntas.")
            
    #Queda perfecto aquí porque valida los números de la entidad Mesa
    def validarMesasNoRepetidas(self, mesa1: Mesa, mesa2: Mesa):
        """Evita que se intente registrar la misma mesa dos veces en el mismo pedido."""
        if mesa2 and mesa1.numero == mesa2.numero:
            raise ValueError("No puedes registrar dos veces la misma mesa en el mismo pedido.")