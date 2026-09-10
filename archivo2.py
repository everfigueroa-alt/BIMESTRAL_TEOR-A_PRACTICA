import tkinter as tk
import random


ventana = tk.Tk()
ventana.title("Pollito Cruzando la Avenida")
ventana.geometry("800x700")
ventana.resizable(False, False)


canvas = tk.Canvas(ventana,width=800,height=700,bg="lightgreen")

canvas.pack()


ancho = 800
alto = 700

velocidad_pollito = 15

juego_terminado = False

carros = []

def crear_escenario():

    # Parte de arriba
    canvas.create_rectangle(
        0, 0,
        800, 100,
        fill="lightgreen",
        outline=""
    )

    # Parte de abajo
    canvas.create_rectangle(
        0, 600,
        800, 700,
        fill="lightgreen",
        outline=""
    )

    # Avenida
    canvas.create_rectangle(
        0, 100,
        800, 600,
        fill="gray"
    )

    # Líneas de la carretera
    for y in range(150, 600, 100):

        for x in range(0, 800, 80):

            canvas.create_rectangle(
                x,
                y,
                x + 40,
                y + 5,
                fill="white",
                outline=""
            )

    # Línea de salida
    canvas.create_rectangle(
        0,
        580,
        800,
        600,
        fill="yellow",
        outline=""
    )

    # Línea de llegada
    canvas.create_rectangle(
        0,
        100,
        800,
        120,
        fill="yellow",
        outline=""
    )

    # Texto
    canvas.create_text(
        400,
        50,
        text="¡LLEVA AL POLLITO AL OTRO LADO!",
        font=("Arial", 20, "bold"),
        fill="darkgreen"
    )


def crear_pollito():

    global pollito

    # Cuerpo
    cuerpo = canvas.create_oval(
        370, 620,
        430, 680,
        fill="yellow",
        outline="black",
        width=2
    )

    # Cabeza
    cabeza = canvas.create_oval(
        380, 600,
        420, 640,
        fill="yellow",
        outline="black",
        width=2
    )

    # Ojo
    ojo = canvas.create_oval(
        405, 610,
        412, 617,
        fill="black"
    )

    # Pico
    pico = canvas.create_polygon(
        420, 620,
        435, 625,
        420, 630,
        fill="orange",
        outline="black"
    )

    # Alas
    ala = canvas.create_oval(
        365, 630,
        385, 650,
        fill="gold",
        outline="black"
    )

    pollito = [
        cuerpo,
        cabeza,
        ojo,
        pico,
        ala
    ]

def crear_carro(x, y, direccion):

    # Carro
    carro = canvas.create_rectangle(
        x,
        y,
        x + 80,
        y + 40,
        fill=random.choice([
            "red",
            "blue",
            "orange",
            "purple",
            "cyan"
        ]),
        outline="black",
        width=2
    )

    # Parte superior
    techo = canvas.create_rectangle(
        x + 15,
        y - 15,
        x + 60,
        y,
        fill="lightblue",
        outline="black"
    )

    # Ruedas
    rueda1 = canvas.create_oval(
        x + 10,
        y + 30,
        x + 30,
        y + 50,
        fill="black"
    )

    rueda2 = canvas.create_oval(
        x + 50,
        y + 30,
        x + 70,
        y + 50,
        fill="black"
    )

    # Guardamos los objetos del carro
    carro_completo = [
        carro,
        techo,
        rueda1,
        rueda2
    ]

    carros.append({
        "objetos": carro_completo,
        "direccion": direccion,
        "velocidad": random.randint(3, 7)
    })

def crear_carros():

    # Carriles que van hacia la derecha
    crear_carro(50, 150, 1)
    crear_carro(400, 250, 1)
    crear_carro(150, 350, 1)
    crear_carro(600, 450, 1)

    # Carriles que van hacia la izquierda
    crear_carro(650, 200, -1)
    crear_carro(300, 300, -1)
    crear_carro(700, 400, -1)
    crear_carro(200, 500, -1)

def mover_pollito(evento):

    if juego_terminado:
        return

    tecla = evento.keysym

    if tecla == "Up": mover_todos(-0, -velocidad_pollito)

    elif tecla == "Down": mover_todos(0, velocidad_pollito)

    elif tecla == "Left": mover_todos(-velocidad_pollito, 0)

    elif tecla == "Right": mover_todos(velocidad_pollito, 0)

    comprobar_limites()
    comprobar_colisiones()

def mover_todos(dx, dy):

    for objeto in pollito: canvas.move(objeto, dx, dy)


def comprobar_limites():

    caja = canvas.bbox(pollito[0])

    if caja is None: return

    x1, y1, x2, y2 = caja

    if x1 < 0:
        mover_todos(-x1, 0)

    if x2 > ancho:
        mover_todos(ancho - x2, 0)

    if y1 < 0:
        mover_todos(0, -y1)

    if y2 > alto:
        mover_todos(0, alto - y2)

def mover_carros():

    if juego_terminado:
        return

    for carro in carros:

        objetos = carro["objetos"]
        direccion = carro["direccion"]
        velocidad = carro["velocidad"]

        for objeto in objetos:

            canvas.move(
                objeto,
                velocidad * direccion,
                0
            )

        # Revisar posición
        caja = canvas.bbox(objetos[0])

        if caja is None:
            continue

        x1, y1, x2, y2 = caja

        # Si sale por la derecha
        if x1 > ancho:

            diferencia = -(x2 + 100)

            for objeto in objetos:
                canvas.move(objeto, diferencia, 0)

        # Si sale por la izquierda
        elif x2 < 0:

            diferencia = ancho - x1 + 100

            for objeto in objetos:
                canvas.move(objeto, diferencia, 0)

    comprobar_colisiones()

    ventana.after(40, mover_carros)

def comprobar_colisiones():

    global juego_terminado

    caja_pollito = canvas.bbox(pollito[0])

    if caja_pollito is None:
        return

    px1, py1, px2, py2 = caja_pollito

    for carro in carros:

        caja_carro = canvas.bbox(carro["objetos"][0])

        if caja_carro is None:
            continue

        cx1, cy1, cx2, cy2 = caja_carro

        # Comprobar si los rectángulos se cruzan
        if (px1 < cx2 and px2 > cx1 and py1 < cy2 and py2 > cy1):
            perder()
            return



    global juego_terminado

    caja = canvas.bbox(pollito[0])

    if caja is None:
        return

    x1, y1, x2, y2 = caja

    # Si llega a la parte superior
    if y1 <= 120:

        juego_terminado = True

        canvas.create_rectangle(200,280,600,420,fill="white",outline="green",width=4)

        canvas.create_text(400,330,text=" ¡GANASTE! ",font=("Arial", 35, "bold"),fill="green")

        canvas.create_text(400,380,text="El pollito cruzó la avenida",font=("Arial", 18),fill="black")


def perder():

    global juego_terminado

    juego_terminado = True

    canvas.create_rectangle(200,280,600,420,fill="white",outline="red",width=4)

    canvas.create_text(400,330,text=" ¡PERDISTE! ",font=("Arial", 35, "bold"),fill="red")

    canvas.create_text(400,380,text="El pollito chocó con un carro",font=("Arial", 18),fill="black")


def reiniciar():

    global juego_terminado
    global carros

    juego_terminado = False

    carros = []

    canvas.delete("all")

    crear_escenario()
    crear_pollito()
    crear_carros()

    mover_carros()

crear_escenario()

crear_pollito()

crear_carros()

ventana.bind("<KeyPress>", mover_pollito)

mover_carros()

ventana.mainloop()