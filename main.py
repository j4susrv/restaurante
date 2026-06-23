import tkinter as tk
# 1. Capa de Validación
from validadores.validador_service import ValidadorService
from restaurante import Restaurante
# 3. Persistencia local y utilidades en la raíz
import repositorio

#Interfaz grafica
from gui.restaurante_gui import RestauranteGUI

#Arranque del Sistema
if __name__ == "__main__":
    root_window = tk.Tk()

    # 1. Instanciamos el cerebro coordinador
    sistema_restaurante = Restaurante()

    # 2. Se lo pasamos a la vista
    app = RestauranteGUI(root_window, sistema_restaurante)

    root_window.mainloop()