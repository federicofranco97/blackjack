import tkinter as tk
import os
from PIL import Image, ImageTk
from guiViewModel import GuiViewModel
from tkinter.scrolledtext import ScrolledText

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

    def __init__(self, model):
    
        self.root = tk.Tk()
        self.cartas = []
        self.score = tk.StringVar()
        self.estado = tk.StringVar()
        self.jugadores = tk.StringVar()
        self.mensajes = tk.StringVar()
        self.app = None
        self.labelScore = None
        self.cartas = None
        self.model = model
        self.textChat = None

        
        self.inicializarFrames()
        self.inicializarBotones()
        self.inicializarEnvioMensajes()  
             
        return
    
    def modoEspera(self):
        
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


        self.frameBotones = tk.Frame(self.framePanelSuperior, width = 1024, height = 30)
        self.frameBotones.pack(side=tk.TOP)
        self.frameBotones['bg']='green'
        self.frameBotones.pack_propagate(0) 
        
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

        self.frameMenuChat = tk.Frame(self.frameInfoDatos, width = 390, height = 511)
        self.frameMenuChat.pack(side=tk.BOTTOM)
        self.frameMenuChat['bg']='white'
        self.frameMenuChat.pack_propagate(0)

        self.frameChat = tk.Frame(self.frameMenuChat, width = 390, height = 451)
        self.frameChat.pack(side=tk.TOP)
        self.frameChat['bg']='white'
        self.frameChat.pack_propagate(0)
        
        self.frameMensaje = tk.Frame(self.frameMenuChat, width = 390, height = 60)
        self.frameMensaje.pack(side=tk.BOTTOM)
        self.frameMensaje['bg']='white'
        self.frameMensaje.pack_propagate(0)

        self.frameMenuEntry = tk.Frame(self.frameMensaje, width = 340, height = 60)
        self.frameMenuEntry.pack(side=tk.LEFT)
        self.frameMenuEntry['bg']='white'
        self.frameMenuEntry.pack_propagate(0)
        
        self.frameMenuButton = tk.Frame(self.frameMensaje, width = 50, height = 60)
        self.frameMenuButton.pack(side=tk.RIGHT)
        self.frameMenuButton['bg']='white'
        self.frameMenuButton.pack_propagate(0)
                        
        return
    
    
    def test(self):
        
        self.cartas = ['1_3', '2_4', '3_5', '4_2', '1_4', '2_2', '1_3', '2_4', '3_5', '4_2', '1_4', '2_2', '1_3', '2_4', '3_5', '4_2', '1_4', '2_2']
        self.cargarCartas(self.cartas)
        #self.modificarScore("20")
        self.modificarScore("20")
        self.modificarEstado("Plantado")
        self.modificarJugadores("Quique: Esperando\nSeba: Esperando\nFede G: Jugando\nFede F: Perdio\nRichard: Esperando")
        self.modificarMensajes("Seba: Esperando...\nQuique: me abuurroonnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn....")
        
        self.model.onPedirCarta()
        print("Test")
        self.mostrar()
        

    def mostrar(self):
        
        self.root.mainloop()
        
        return


    def inicializarBotones(self):

        ancho = 13
        colorFront = "white"
        colorBack = "medium blue"
        self.buttonConectar= tk.Button(self.frameBotones, width = ancho, height = 20,
                           text="CONECTAR",
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", 9),
                           command=self.btConectar)
        self.buttonConectar.pack(side=tk.LEFT)
        self.buttonIngresar = tk.Button(self.frameBotones, width = ancho, height = 20, 
                           text="INGRESAR", 
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", 9),
                           command=self.btIngresar)
        self.buttonIngresar.pack(side=tk.LEFT)
        self.buttonPedir = tk.Button(self.frameBotones, width = ancho, height = 20,
                           text="PEDIR", 
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", 9),
                           command=self.btPedir)
        self.buttonPedir.pack(side=tk.LEFT)
        self.buttonPlantarse = tk.Button(self.frameBotones, width = ancho, height = 20,
                           text="PLANTARSE", 
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", 9),
                           command=self.btPlantarse)
        self.buttonPlantarse.pack(side=tk.LEFT)
        self.buttonSeparar = tk.Button(self.frameBotones, width = ancho, height = 20,
                           text="SEPARAR",
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", 9),
                           command=self.btSeparar)
        self.buttonSeparar.pack(side=tk.LEFT)
        self.buttonApostar = tk.Button(self.frameBotones, width = ancho, height = 20,
                           text="APOSTAR", 
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", 9),
                           command=self.btApostar)
        self.buttonApostar.pack(side=tk.LEFT)
        self.labelPesos = tk.Label(self.frameBotones, text="$",width = 3, height = 20,
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", 9))
        self.labelPesos.pack(side=tk.LEFT)
        self.scrolledMonto = tk.Text(self.frameBotones, width = 8, height = 18, 
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", 15))
        self.scrolledMonto.pack(side=tk.LEFT)
        self.buttonFondear = tk.Button(self.frameBotones, width = ancho, height = 20,
                           text="FONDEAR", 
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", 9),
                           command=self.btFondear)
        self.buttonFondear.pack(side=tk.LEFT)
        self.buttonDoblar = tk.Button(self.frameBotones, width = ancho, height = 20,
                           text="DOBLAR", 
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", 9),
                           command=self.btDoblar)
        self.buttonDoblar.pack(side=tk.LEFT)
        self.buttonSalir = tk.Button(self.frameBotones, width = ancho, height = 20,
                           text="SALIR", 
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", 9),
                           command=quit)
        self.buttonSalir.pack(side=tk.LEFT)
        
        return

    def btConectar(self):
        
        #self.model.onConecta()
       
        return
    
    
    def btIngresar(self):
        
        self.model.onPedirCarta()
       
        return
    
    
    def btPedir(self):
 
        self.model.onPedirCarta()
       
        return
    
    
    def btPlantarse(self):
        
        self.model.onPlantarse()
       
        return
    
    
    def btSeparar(self):
        
        self.model.onSeparar()
       
        return
    
    
    def btFondear(self):
        
        monto = self.scrolledMonto.get("1.0", tk.END)
        self.model.onFondear(monto)
        self.scrolledMonto.delete("0.0", tk.END)
       
        return
    
    
    def btApostar(self):
        
        monto = self.scrolledMonto.get("1.0", tk.END)
        self.model.onApostar(monto)
        self.scrolledMonto.delete("0.0", tk.END)
       
        return
    
    
    def btDoblar(self):
        
        self.model.onDoblar()
       
        return    

    
    def enviarMensaje(self):
        
        mensaje = self.entryEnvioMensajes.get("1.0", tk.END)
        self.entryEnvioMensajes.delete("0.0", tk.END)
        self.modificarMensajes(mensaje)
        self.model.onEnviarMensaje(mensaje)
                
        return


    def inicializarEnvioMensajes(self):
      
        self.entryEnvioMensajes = ScrolledText(self.frameMenuEntry, 
                                    font=("Arial Bold", 10))
        self.entryEnvioMensajes.pack()

        self.buttonEnviarMensaje = tk.Button(self.frameMenuButton, width = 48, height = 48,
                           text="ENVIAR", 
                           fg="white",
                           bg="medium blue",
                           command=self.enviarMensaje)
        self.buttonEnviarMensaje.pack()
        
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
        
        #self.jugadores.set(jugadores)
        self.textJugadores.insert(tk.END, jugadores)
        self.textJugadores.see(tk.END)
                
        return
        
    
    def cargarJugadores(self, jugadores):

        self.scrollbarJugadores = tk.Scrollbar(self.frameJugadores) 
        self.textJugadores = tk.Text(self.frameJugadores, width = 622, height = 148,
                                font=("Arial Bold", 15), fg="black", bg="white")
        self.scrollbarJugadores.pack(side=tk.RIGHT, fill=tk.Y)
        self.textJugadores.pack(side=tk.LEFT, fill=tk.Y)
        self.scrollbarJugadores.config(command=self.textJugadores.yview)
        self.textJugadores.config(yscrollcommand=self.scrollbarJugadores.set)

        self.modificarJugadores(jugadores)
        self.textJugadores.pack(side=tk.LEFT)

        return

    
    def modificarMensajes(self, mensajes):
        
        #self.mensajes.set(mensajes)
        self.textChat.insert(tk.END, mensajes)
        self.textChat.see(tk.END)
        
        return
        
    
    def cargarMensajes(self, mensajes):

        self.scrollbarChat = tk.Scrollbar(self.frameChat) 
        self.textChat = tk.Text(self.frameChat, width=388, height=449,
                                font=("Arial Bold", 10), fg="black", bg="white")
        self.scrollbarChat.pack(side=tk.RIGHT, fill=tk.Y)
        self.textChat.pack(side=tk.LEFT, fill=tk.Y)
        self.scrollbarChat.config(command=self.textChat.yview)
        self.textChat.config(yscrollcommand=self.scrollbarChat.set)

        self.modificarMensajes(mensajes)
        self.textChat.pack(side=tk.LEFT)

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
        yLineOffset = 60
        x = x0
        y = y0
        cartasPorLinea = 7
        for i in range(0, len(self.cartas)):
            self.imgList.append(os.path.join(os.path.join(self.cwd, mazo), self.cartas[i] + '.jpg'))
            self.app.agregar(self.imgList[i], x, y)

            x = x + xOffset
            y = y + yOffset
            if (i+1) % cartasPorLinea == 0:
                x = x0
                y = y0 + int((i/cartasPorLinea)*yLineOffset)
 
        return

def pedirCarta():
    print("hola carta")

if __name__ == "__main__":
    #cartas1 = ['1_3', '2_4', '3_5']
    listaCartas = ['1_3', '2_4', '3_5', '4_2', '1_4', '2_2']
    
    
    model = GuiViewModel()
    model.ee.on("pedirCartaEvent", pedirCarta)
    
    bjScreen = PantallaPrincipal(model)
    bjScreen.cargarCartas(listaCartas)
    bjScreen.cargarScore("12")
    bjScreen.cargarEstado("Jugar")
    bjScreen.cargarJugadores("Quique: Esperando\nSeba: Esperando\nFede G: Esperando\nFede F: Jugando\nRichard: Esperando")
    bjScreen.cargarMensajes("Quique: Esperando...\n")
    listaCartas = ['1_3', '2_4', '3_5']
    bjScreen.mostrar()
    
    test=input("prueba")
    
