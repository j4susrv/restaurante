# Clase Pedido
from entidades.pedido import Pedido

# Clase encargada de validar pedidos
class ValidadorPedido:
    # Verifica que el pedido exista
    def validarPedido(self, pedido: Pedido):
        if pedido is None:
            raise ValueError("El pedido solicitado no existe.")
    # Verifica que el pedido siga abierto
    def validarPedidoAbierto(self, pedido: Pedido):
        self.validarPedido(pedido)
        estado_actual = pedido.estado.lower().strip()
        if estado_actual != "abierto":
            raise ValueError(f"El pedido #{pedido.id} ya está {pedido.estado}. No se puede modificar.")

    # Valida el nombre del cliente
    def validarCliente(self, cliente: str):
        # Verifica que no esté vacío
        if not cliente or cliente.strip() == "":
            raise ValueError("El nombre del cliente no puede estar vacío.")
        # Elimina espacios extras
        palabras = cliente.strip().split()
        # Une nuevamente el nombre con un solo espacio
        nombre_corregido = " ".join(palabras)
        # Crea una versión sin espacios para medir caracteres reales
        nombre_sin_espacios = nombre_corregido.replace(" ", "")
        # Verifica largo mínimo y máximo
        if len(nombre_sin_espacios) < 5:
            raise ValueError("El nombre debe tener más caracteres reales.")
        if len(nombre_sin_espacios) > 50:
            raise ValueError("El nombre no puede tener más de 50 caracteres.")
        # Verifica que solo tenga letras y espacios
        for letra in nombre_corregido.lower():
            if not (
                 # Verifica que cada carácter sea:
                # - una letra
                # - un espacio
                # - o una vocal con tilde / ñ / ü
                letra.isalpha() #Solo letras
                or letra == ' '
                or letra in "áéíóúñü"
            ):
                raise ValueError("El nombre solo puede contener letras y espacios.")
        # Verifica cantidad de palabras
        cantidad_palabras = len(palabras)
        if cantidad_palabras < 2:
            raise ValueError("Debe ingresar al menos un nombre y un apellido (mínimo 2 palabras).")
        if cantidad_palabras > 4:
            raise ValueError("El nombre es demasiado largo. Ingrese un máximo de 4 palabras.")
        # Lista de palabras no permitidas
        palabras_basura = [
            "mesa", "mesas", "plato", "platos",
            "pedido", "boleta", "jaja", "jiji", "asdasd"
        ]
        # Verifica palabras prohibidas
        for p in palabras:
            if p.lower() in palabras_basura:
                raise ValueError(f"La palabra '{p}' no está permitida como nombre de cliente.")
        return nombre_corregido

    # Verifica si el pedido puede cancelarse
    def validarCancelacion(self, pedido: Pedido):
        self.validarPedido(pedido)
        # No permite cancelar pedidos cerrados
        if pedido.estado == "cerrado":
            raise ValueError("No se puede cancelar un pedido que ya ha sido facturado y cerrado.")

        # Verifica si ya estaba cancelado
        if pedido.estado == "cancelado":
            raise ValueError("El pedido ya se encuentra cancelado.")
    def validarNota(self, nota: str, campo: str = "Nota"):

        if nota is None:
            raise ValueError(f"El campo {campo} no puede ser nulo.")