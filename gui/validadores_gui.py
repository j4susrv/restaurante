"""
gui/validadores_gui.py
Responsabilidad única: Generar comandos de validación de entrada
para los campos de texto de la interfaz Tkinter (SRP).
"""
#Se encarga de generar comandos de validacion de entrada para los campos de texto

class ValidadoresGUI:
    """Fábrica de comandos de validación para widgets Entry de Tkinter."""

    @staticmethod
    def crear_validador_texto_cliente(ventana):
        """Genera un comando de registro para validar que solo se escriban letras y espacios."""
        def validar_entrada(texto_nuevo):
            if texto_nuevo == "":
                return True
            if len(texto_nuevo) > 35:
                return False
            if "  " in texto_nuevo:
                return False
            return all(c.isalpha() or c.isspace() for c in texto_nuevo)

        return ventana.register(validar_entrada)

    @staticmethod
    def crear_validador_notas(ventana):
        """Genera un comando de registro para validar las notas del pedido."""
        def validar_notas(texto_nuevo):
            if texto_nuevo == "":
                return True
            if len(texto_nuevo) > 100:
                return False
            if "  " in texto_nuevo:
                return False

            # CARACTERES PERMITIDOS: Solo letras, números y espacios individuales.
            # No incluye puntos ni símbolos especiales, bloqueándolos de inmediato.
            for caracter in texto_nuevo:
                es_letra_o_numero = caracter.isalnum()
                es_tilde_o_enie = caracter.lower() in "áéíóúñü"
                es_espacio = caracter == ' '

                if not (es_letra_o_numero or es_tilde_o_enie or es_espacio):
                    return False
            return True

        return ventana.register(validar_notas)