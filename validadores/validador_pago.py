class ValidadorPago:
    
    def validarTipoPago(self, tipoPago: str):
        tipos_validos = ["efectivo", "tarjeta", "transferencia"]
        if not tipoPago or tipoPago.lower().strip() not in tipos_validos:
            raise ValueError(f"Tipo de pago '{tipoPago}' no es válido. Use: efectivo, tarjeta o transferencia.")

    """def validarPropina(self,monto_propina: int, tipo_pago: str, monto_subtotal: int):
        if monto_propina < 0:
            raise ValueError("El monto de la propina no puede ser un valor negativo.")
        
        monto_total = monto_subtotal + monto_propina
        
        if tipo_pago.lower().strip() == "efectivo":
            return
        Limites = {"tarjeta":400000,"transferencia":200000}
        if monto_total > Limites.get(tipo_pago.lower(), int()):
            raise ValueError(f"El monto total (subtotal + propina) excede el limite {tipo_pago}")"""
        
        

    def validarLimitePago(self, tipoPago: str, monto: int):
        """
        Valida que el monto sea permitido según el método de pago:
        - tarjeta: máximo 400000
        - transferencia: máximo 200000
        - efectivo: sin límite
        Lanza ValueError con un mensaje claro si excede el límite.
        """
        if monto is None:
            return
        t = tipoPago.lower().strip() if tipoPago else ""
        if t == "tarjeta":
            print(monto)
            max_tarjeta = 400000
            if monto > max_tarjeta:
                from utils_format import formato_moneda
                raise ValueError(f"Pago con TARJETA no permitido. Monto máximo: ${formato_moneda(max_tarjeta)}.")
                
        elif t == "transferencia":
            max_transferencia = 200000
            if monto > max_transferencia:
                from utils_format import formato_moneda
                raise ValueError(f"Pago por TRANSFERENCIA no permitido. Monto máximo: ${formato_moneda(max_transferencia)}.")
        return f"Monto completo {monto}"

        # efectivo y otros tipos no tienen límite adicional aquí
