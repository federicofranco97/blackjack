from tkinter import Tk, Label

labelTitulo = None


def mostrarInterfaz(view):
    root = Tk()
    root.title("BLACKJACK")
    root.geometry("1000x700+50+50")

    # Create a label as a child of root window
    labelTitulo = Label(root, text=view.Jugador)
    labelTitulo.pack()

    root.mainloop()



def setTurnoActual(jugador):
    if labelTitulo == None:
        return
    labelTitulo.setvar(jugador)