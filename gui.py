import os
import time
import tkinter as tk
from _thread import start_new_thread
import playsound


def mostrarInterfaz(view):
    root = tk.Tk()
    root.title("BLACKJACK")
    root.geometry("1000x700+50+50")

    FrameBotones = tk.Frame(root)
    FrameBotones.pack()

    btnApostar = tk.Button(FrameBotones, text="APOSTAR", fg="red", command=lambda: TestMethod(view))
    btnApostar.pack(side=tk.LEFT)

    btnPedir = tk.Button(FrameBotones, text="PEDIR", fg="red", command=lambda: TestMethod(view), state="disabled")
    btnPedir.pack(side=tk.LEFT)

    btnPlantarse = tk.Button(FrameBotones, text="PLANTARSE", fg="red", command=lambda: TestMethod(view))
    btnPlantarse.pack(side=tk.LEFT)

    titulo = tk.StringVar()
    labelTitulo = tk.Label(root, textvariable=titulo)
    labelTitulo.pack()

    miscartas = tk.StringVar()
    labelCartas = tk.Label(root, textvariable=miscartas)
    labelCartas.pack()

    #view.observe('refreshButtonsEvent', lambda: RefreshButtonsStatus(view, btnApostar, btnPedir, btnPlantarse))

    #start_new_thread(refreshGUI,(view, titulo, miscartas))

    root.mainloop()

def TestMethod(view):
    print('asd')
    start_new_thread(play, ())
    view.onPedirCarta()

def RefreshButtonsStatus(view, btnApostar, btnPedir, btnPlantarse):
    if "apostar" in view.Acciones:
        btnApostar.config(state="normal")
    else:
        btnApostar.config(state="disabled")

    if "pedir" in view.Acciones:
        btnPedir.config(state="normal")
    else:
        btnPedir.config(state="disabled")

    if "plantarse" in view.Acciones:
        btnPlantarse.config(state="normal")
    else:
        btnPlantarse.config(state="disabled")

def play():
    soundurl = os.path.join("sounds", "myTurn.mp3")
    playsound.playsound(soundurl)

def refreshGUI(pView, pTitulo, pMisCartas):
    while True:
        #time.sleep(1000)
        pTitulo.set(pView.Turno)
        pMisCartas.set(pView.MisCartas)



