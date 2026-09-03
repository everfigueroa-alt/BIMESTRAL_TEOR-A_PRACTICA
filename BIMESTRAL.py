from tkinter import *
import random

# -----------------
# ventana principal
# -----------------
ventana_principal = Tk()
ventana_principal.title("Game Pollito")
ventana_principal.resizable(False, False)
ventana_principal.geometry("700x500")
ventana_principal.config(bg="white")

# frame de graficacion
frame_graficacion = Frame(ventana_principal)
frame_graficacion.config(bg="white", width=650, height=450)
frame_graficacion.place(x=10,y=10)

# creacion canvas
c = Canvas(frame_graficacion, width=650, height=450)
c.config(bg="green")
c.place(x=10,y=10)


#-----------------
# FUNCIONES 
#-----------------


# Función para crear pollito
def crear_pollito():
    pollito = c.create_oval(pollito_x - radio_pollito, pollito_y - radio_pollito, pollito_x + radio_pollito, pollito_y + radio_pollito, fill="yellow")

# Función para crear carros 
def crear_carros():
    pass

# Función para mover hacia abajo
def mover_abajo():
    pass

# Función para mover hacia arriba
def mover_arriba():
    pass

# ubicacion inicial pollito
pollito_x = 300
pollito_y = 650

radio_pollito = 18

# Vidas y Victorias
vidas = 5
victorias = 0   
juego_activo = True

ventana_principal.mainloop()