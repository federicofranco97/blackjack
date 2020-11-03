import tkinter as tk
import os
from PIL import Image, ImageTk

class PantallaCartas(tk.Frame):
    
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=1)
        self.img = []

        return

    def agregar(self, img, x=0, y=0):
    
        self.img.append(img)
        pos = len(self.img)-1
        
        load = Image.open(self.img[pos])
        render = ImageTk.PhotoImage(load)
        self.img[pos] = tk.Label(self.master, image=render)
        self.img[pos].image = render
        self.img[pos].place(x=x, y=y)
        
        return

    def borrar(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        
        return


class PantallaPrincipal:

    def __init__(self):
    
        self.root = tk.Tk()
        self.cartas = []
        self.score = tk.StringVar()
        self.estado = tk.StringVar()
        self.jugadores = tk.StringVar()
        self.mensajes = tk.StringVar()
        self.app = None
        self.labelScore = None
        self.cartas = None

        
        self.inicializarFrames()
        self.inicializarBotones()
        
        return
    

    def inicializarFrames(self):
        
        #https://www.tutorialspoint.com/python/tk_button.htm
        self.root.wm_title("Blackjac UB version Betal Alfa Centauri v1.0.1")
        self.root.geometry("1024x768")
        self.root['bg']='green'
 

        self.framePanelSuperior = tk.Frame(self.root, width = 1024, height = 718)
        self.framePanelSuperior.pack(side=tk.TOP)
        self.framePanelSuperior['bg']='green'

        self.framePanelInferior = tk.Frame(self.root, width = 1024, height = 50)
        self.framePanelInferior.pack(side=tk.BOTTOM)
        self.framePanelInferior['bg']='green'


        self.frameBotones = tk.Frame(self.framePanelSuperior, width = 1024, height = 50)
        self.frameBotones.pack(side=tk.TOP)
        self.frameBotones['bg']='green'
        
        self.framePanel = tk.Frame(self.framePanelSuperior, width = 1024, height = 668)
        self.framePanel.pack(side=tk.BOTTOM)
        self.framePanel['bg']='green'
        
 
        self.frameTablero = tk.Frame(self.framePanel, width = 624, height = 668)
        self.frameTablero.pack(side=tk.LEFT)
        self.frameTablero['bg']='green'

        self.frameInfo = tk.Frame(self.framePanel, width = 400, height = 668)
        self.frameInfo.pack(side=tk.RIGHT)
        self.frameInfo['bg']='green'       

        self.frameJuego = tk.Frame(self.frameTablero, width = 624, height = 518)
        self.frameJuego.pack(side=tk.TOP)
        self.frameJuego['bg']='green'
        
        self.frameCartas = tk.Frame(self.frameJuego, width = 624, height = 468)
        self.frameCartas.pack(side=tk.TOP)
        self.frameCartas['bg']='green'
        self.frameCartas.pack_propagate(0)      
 
        self.frameEstado = tk.Frame(self.frameJuego, width = 624, height = 50)
        self.frameEstado.pack(side=tk.BOTTOM)
        self.frameEstado['bg']='medium blue' 
        self.frameEstado.pack_propagate(0)      

        
        self.frameJugadores = tk.Frame(self.frameTablero, width = 624, height = 150)
        self.frameJugadores.pack(side=tk.BOTTOM)
        self.frameJugadores['bg']='white'
        self.frameJugadores.pack_propagate(0)
 
 
        self.frameInfoAuxiliar = tk.Frame(self.frameInfo, width = 2, height = 668)
        self.frameInfoAuxiliar.pack(side=tk.LEFT)
        self.frameInfoAuxiliar['bg']='green'

        self.frameInfoDatos = tk.Frame(self.frameInfo, width = 398, height = 668)
        self.frameInfoDatos.pack(side=tk.RIGHT)
        self.frameInfoDatos['bg']='green'

        self.frameScoreContexto = tk.Frame(self.frameInfoDatos, width = 390, height = 150)
        self.frameScoreContexto.pack(side=tk.TOP)
        self.frameScoreContexto['bg']='medium blue'
        
        self.frameScore = tk.Frame(self.frameScoreContexto, width = 390, height = 148)
        self.frameScore.pack(side=tk.TOP)
        self.frameScore['bg']='medium blue'

        self.frameScoreSeparador = tk.Frame(self.frameScoreContexto, width = 390, height = 2)
        self.frameScoreSeparador.pack(side=tk.BOTTOM)
        self.frameScoreSeparador['bg']='green'

        self.frameChat = tk.Frame(self.frameInfoDatos, width = 390, height = 511)
        self.frameChat.pack(side=tk.BOTTOM)
        self.frameChat['bg']='white'
        self.frameChat.pack_propagate(0)

        return 
    
    
    def test(self):
        
        self.cargarCartas(self.cartas)
        #self.modificarScore("20")
        self.modificarScore("20")
        self.modificarEstado("Plantado")
        self.modificarJugadores("Quique: Esperando\nSeba: Esperando\nFede G: Jugando\nFede F: Perdio\nRichard: Esperando")
        self.modificarMensajes("Seba: Esperando...\nQuique: me abuurroo....")
        print("Test")
        self.mostrar()
        

    def mostrar(self):
        
        self.root.mainloop()
        
        return


    def inicializarBotones(self):

        frame = self.frameBotones
        button1 = tk.Button(frame, 
                           text="CONECTAR", 
                           fg="red",
                           command=self.test)
        button1.pack(side=tk.LEFT)
        button2 = tk.Button(frame, 
                           text="INGRESAR", 
                           fg="red",
                           command=self.test)
        button2.pack(side=tk.LEFT)
        button3 = tk.Button(frame, 
                           text="APOSTAR", 
                           fg="red",
                           command=self.test)
        button3.pack(side=tk.LEFT)
        button4 = tk.Button(frame, 
                           text="PLANTARSE", 
                           fg="red",
                           command=self.test)
        button4.pack(side=tk.LEFT)
        slogan = tk.Button(frame,
                           text="MENSAJE",
                           command=self.test)
        slogan.pack(side=tk.LEFT)
        button5 = tk.Button(frame, 
                           text="SALIR", 
                           fg="red",
                           command=quit)
        button5.pack(side=tk.LEFT)
        
        return
    
    def modificarScore(self, score):
        
        self.score.set(score)
        
        return
        
    
    def cargarScore(self, score):
        
        self.modificarScore(score)
        self.labelScore = tk.Label(self.frameScore, textvariable=self.score, 
                                   font=("Arial Bold", 100), bg="medium blue", fg="white")
        self.labelScore.pack(side=tk.TOP)

        return

    
    def modificarEstado(self, estado):
        
        self.estado.set(estado)
        
        return
        
    
    def cargarEstado(self, estado):
        
        self.modificarEstado(estado)
        self.labelScore = tk.Label(self.frameEstado, textvariable=self.estado, 
                                   font=("Arial Bold", 30), bg="medium blue", fg="white")
        self.labelScore.pack()

        return


    def modificarJugadores(self, jugadores):
        
        self.jugadores.set(jugadores)
        
        return
        
    
    def cargarJugadores(self, jugadores):
        
        self.modificarJugadores(jugadores)
        self.labelScore = tk.Label(self.frameJugadores, textvariable=self.jugadores, 
                                   font=("Arial Bold", 20), fg="black", bg="white", justify=tk.LEFT)
        self.labelScore.pack(side=tk.LEFT)

        return

    
    def modificarMensajes(self, mensajes):
        
        self.mensajes.set(mensajes)
        
        return
        
    
    def cargarMensajes(self, mensajes):
        
        self.modificarMensajes(mensajes)
        self.labelScore = tk.Label(self.frameChat, textvariable=self.mensajes, 
                                   font=("Arial Bold", 10), fg="medium blue", bg="white", justify=tk.LEFT)
        self.labelScore.pack(side=tk.LEFT)

        return

    
    def cargarCartas(self, cartas):
        
        if self.app == None:
            self.app = PantallaCartas(self.frameCartas)
            self.app['bg']='green'
        else:
            self.app.borrar()
        
        self.cartas = cartas
        self.cwd = os.getcwd()
        mazo = 'mazo'
        self.imgList = []
        x0 = 20
        y0 = 5
        xOffset = 60
        yOffset = 5
        yLineOffset = 100
        x = x0
        y = y0
        cartasPorLinea = 7
        for i in range(0, len(self.cartas)):
            self.imgList.append(os.path.join(os.path.join(self.cwd, mazo), self.cartas[i] + '.jpg'))
            '''225 x 315
               640 x 480'''
                          
            print(x, y)
            self.app.agregar(self.imgList[i], x, y)

            x = x + xOffset
            y = y + yOffset
            if (i+1) % cartasPorLinea == 0:
                x = x0
                y = y0 + int((i/cartasPorLinea)*yLineOffset)
 
        return



if __name__ == "__main__":
    #cartas1 = ['1_3', '2_4', '3_5']
    listaCartas = ['1_3', '2_4', '3_5', '4_2', '1_4', '2_2']
    
    bjScreen = PantallaPrincipal()
    bjScreen.cargarCartas(listaCartas)
    bjScreen.cargarScore("12")
    bjScreen.cargarEstado("Jugar")
    bjScreen.cargarJugadores("Quique: Esperando\nSeba: Esperando\nFede G: Esperando\nFede F: Jugando\nRichard: Esperando")
    bjScreen.cargarMensajes("Quique: Esperando...")
    listaCartas = ['1_3', '2_4', '3_5']
    bjScreen.mostrar()
    
    test=input("prueba")
