import tkinter as tk
#import os
import playsound
from Pantalla import MostrarImagenes 
#from PIL import Image, ImageTk
#from guiViewModel import GuiViewModel
#from tkinter.scrolledtext import ScrolledText
#from _thread import *

class Ingresar:

    def __init__(self, model):
        
        self.root = tk.Tk()
        self.model = model

        self.inicializarFrames()
        self.cargarImagen()
        self.configurarEventos()

        return
    

    def inicializarFrames(self):
                
        color = 'medium blue'        
        self.root.wm_title("Blackjac UB version Betal Alfa Centauri v1.0.1")
        self.root.geometry("1024x768")
        self.root['bg']=color
 
        self.framePanelTitulo = tk.Frame(self.root, width = 1024, height = 150)
        self.framePanelTitulo.pack(side=tk.LEFT)
        self.framePanelTitulo['bg']=color
        self.framePanelTitulo.pack_propagate(0)
        
        self.framePanelConexion = tk.Frame(self.root, width = 1024, height = 618)
        self.framePanelConexion.pack(side=tk.RIGHT)
        self.framePanelConexion['bg']=color
        self.framePanelConexion.pack_propagate(0)
    
    
        self.framePanelDatos = tk.Frame(self.framePanelConexion, width = 324, height = 618)
        self.framePanelDatos.pack(side=tk.LEFT)
        self.framePanelDatos['bg']=color
        self.framePanelDatos.pack_propagate(0)
        
        self.framePanelImagen = tk.Frame(self.framePanelConexion, width = 700, height = 618)
        self.framePanelImagen.pack(side=tk.RIGHT)
        self.framePanelImagen['bg']=color
        self.framePanelImagen.pack_propagate(0)

        self.frameConexion = tk.Frame(self.framePanelDatos, width = 400, height = 30)
        self.frameConexion.pack(side=tk.TOP)
        self.frameConexion['bg']=color
        self.frameConexion.pack_propagate(0)

        self.frameIngreso = tk.Frame(self.framePanelDatos, width = 300, height = 30)
        self.frameIngreso.pack(side=tk.BOTTOM)
        self.frameIngreso['bg']=color
        self.frameIngreso.pack_propagate(0) 


        self.frameServidor = tk.Frame(self.frameConexion, width = 300, height = 30)
        self.frameServidor.pack(side=tk.TOP)
        self.frameServidor['bg']=color
        self.frameServidor.pack_propagate(0)

        self.frameConectar = tk.Frame(self.frameConexion, width = 100, height = 30)
        self.frameConectar.pack(side=tk.TOP)
        self.frameConectar['bg']=color
        self.frameConectar.pack_propagate(0)


        self.frameDireccionIP = tk.Frame(self.frameServidor, width = 150, height = 30)
        self.frameDireccionIP.pack(side=tk.TOP)
        self.frameDireccionIP['bg']=color
        self.frameDireccionIP.pack_propagate(0)

        self.framePuerto = tk.Frame(self.frameServidor, width = 150, height = 30)
        self.framePuerto.pack(side=tk.TOP)
        self.framePuerto['bg']=color
        self.framePuerto.pack_propagate(0)

        
        self.frameUsuario = tk.Frame(self.frameIngreso, width = 150, height = 30)
        self.frameUsuario.pack(side=tk.TOP)
        self.frameUsuario['bg']=color
        self.frameUsuario.pack_propagate(0)

        self.frameIngresar = tk.Frame(self.frameIngreso, width = 100, height = 30)
        self.frameIngresar.pack(side=tk.TOP)
        self.frameIngresar['bg']=color
        self.frameIngresar.pack_propagate(0)
        
        return


    def notificacion(self, usuario):
        
        if (usuario == self.usuario):
            start_new_thread(self.play, ())
        
        return


    def play(self):
        
        soundurl = os.path.join("sounds", "messageEntered.mp3")
        playsound.playsound(soundurl)
        
        return


    def cargarImagen(self):

        self.app = MostrarImagenes(self.frameImagen)
        self.app['bg']='green'
        
        self.imagen = 'blackjack'
        self.cwd = os.getcwd()
        images = 'images'
        x = 400
        y = 400
        
        self.imgList.append(os.path.join(os.path.join(self.cwd, images), self.imagen + '.jpg'))
        self.app.agregar(self.imagen, x, y)
 
        return




class PantallaPrincipal:

    def __init__(self, model, usuario):
    
        self.root = tk.Tk()
        self.cartas = []
        self.score = tk.StringVar()
        self.usuario = usuario
        self.estado = tk.StringVar()
        self.estadoStr = ""
        self.jugadores = tk.StringVar()
        self.mensajes = tk.StringVar()
        self.app = None
        self.labelScore = None
        self.cartas = None
        self.model = model
        self.textChat = None
        #self.modificarUsuario(self.usuario)
        
        self.inicializarFrames()
        self.inicializarBotones()
        self.inicializarEnvioMensajes()  
        self.cargarScore("0")
        self.cargarEstado("...")
        self.cargarJugadores("")
        self.cargarBotones("")
        self.habilitarBotones()
        self.cargarMensajes("")
        
        self.configurarEventos()
        
        return

    def cambioTurno(self, usuario):
        
        if (usuario == self.usuario):
            start_new_thread(self.play, ())
        
        return
    
    def play(self):
        
        soundurl = os.path.join("sounds", "myTurn.mp3")
        playsound.playsound(soundurl)
        
        return


    def configurarEventos(self):

        self.model.ee.on("refreshButtonsEvent", self.cargarBotones)
        self.model.ee.on("turnoChangedEvent", self.cambioTurno)
        self.model.ee.on("mensajeEntranteEvent", self.modificarMensajes)
        self.model.ee.on("estadoChangedEvent", self.modificarEstado)
        self.model.ee.on("juegoComenzadoEvent", self.modificarEstado)
        self.model.ee.on("juegoTerminadoEvent", self.modificarEstado)
        self.model.ee.on("jugadoresRefreshedEvent", self.modificarJugadores)
        #self.model.ee.on("puntajeBancaChangedEvent", self.modificarScore)

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
 
        #self.frameEstadoUsuario = tk.Frame(self.frameJuego, width = 624, height = 50)
        #self.frameEstadoMenu.pack(side=tk.BOTTOM)
        #self.frameEstadoMenu['bg']='medium blue' 
        #self.frameEstadoMenu.pack_propagate(0)      

        #self.frameNombreUsuario = tk.Frame(self.frameEstadoMenu, width = 200, height = 50)
        #self.frameNombreUsuario.pack(side=tk.LEFT)
        #self.frameNombreUsuario['bg']='medium blue' 
        #self.frameNombreUsuario.pack_propagate(0)  
        
        self.frameEstadoUsuario = tk.Frame(self.frameJuego, width = 624, height = 50)
        self.frameEstadoUsuario.pack(side=tk.RIGHT)
        self.frameEstadoUsuario['bg']='medium blue' 
        self.frameEstadoUsuario.pack_propagate(0)  

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
            

    def cargarBotones(self, botones):
        
        self.botones = botones
        self.habilitarBotones()
        self.modificarEstado(self.estadoStr)
        
        return
    

    def habilitarBotones(self):

        self.botonesActivados = {"ingresar": False,
                                 "apostar": False,
                                 "doblar": False,
                                 "pedir": False,
                                 "separar": False,
                                 "plantarse": False,
                                 "mensaje": False}
        
        
        for boton in self.botones:
            
            self.botonesActivados[boton] = True
        
        for boton in self.botonesActivados:
            self.habilitarBoton(boton, self.botonesActivados[boton])
        
        return
    

    def habilitarBoton(self, boton, activar):
       
        estado = "disabled"
        if activar:
            estado = "normal"

        if boton == "ingresar":
            self.buttonIngresar.config(state=estado)
        elif boton == "apostar":
            self.buttonApostar.config(state=estado)
        elif boton == "pedir":
            self.buttonPedir.config(state=estado)
        elif boton == "plantarse":
            self.buttonPlantarse.config(state=estado)
        elif boton == "separar":
            self.buttonSeparar.config(state=estado)
        elif boton == "doblar":
            self.buttonDoblar.config(state=estado)
        elif boton == "mensaje":
            self.buttonEnviarMensaje.config(state=estado)
        
        return
    

    def mostrar(self):
        
        self.root.mainloop()
        
        return
    
    def procesarMonto(self, monto):
        
        if self.botonesActivados['apostar']:
            self.btApostar()
        elif self.botonesActivados['ingresar']:
            self.btIngresar()


    def inicializarBotones(self):

        ancho = 14
        colorFront = "white"
        colorBack = "medium blue"
        tamLetra = 13
        tamMonto = 15
        #self.buttonConectar= tk.Button(self.frameBotones, width = ancho, height = 20,
        #                   text="CONECTAR",
        #                   fg=colorFront,
        #                   bg=colorBack,
        #                   font=("Arial Bold", 9),
        #                   command=self.btConectar)
        #self.buttonConectar.pack(side=tk.LEFT)
        self.buttonIngresar = tk.Button(self.frameBotones, width = ancho, height = 20, 
                           text="INGRESAR", 
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra),
                           command=self.btIngresar)
        self.buttonIngresar.pack(side=tk.LEFT)
        self.labelPesos = tk.Label(self.frameBotones, text="$",width = 1, height = 20,
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra))
        self.labelPesos.pack(side=tk.LEFT)
        self.scrolledMonto = tk.Text(self.frameBotones, width = 6, height = 18, 
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamMonto))
        self.scrolledMonto.bind('<Return>', self.procesarMonto)
        self.scrolledMonto.pack(side=tk.LEFT)
        self.buttonApostar = tk.Button(self.frameBotones, width = ancho, height = 20,
                           text="APOSTAR", 
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra),
                           command=self.btApostar)
        self.buttonApostar.pack(side=tk.LEFT)
        self.buttonPedir = tk.Button(self.frameBotones, width = ancho, height = 20,
                           text="PEDIR", 
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra),
                           command=self.btPedir)
        self.buttonPedir.pack(side=tk.LEFT)
        self.buttonPlantarse = tk.Button(self.frameBotones, width = ancho, height = 20,
                           text="PLANTARSE", 
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra),
                           command=self.btPlantarse)
        self.buttonPlantarse.pack(side=tk.LEFT)
        self.buttonSeparar = tk.Button(self.frameBotones, width = ancho, height = 20,
                           text="SEPARAR",
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra),
                           command=self.btSeparar)
        self.buttonSeparar.pack(side=tk.LEFT)
        self.buttonDoblar = tk.Button(self.frameBotones, width = ancho, height = 20,
                           text="DOBLAR", 
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra),
                           command=self.btDoblar)
        self.buttonDoblar.pack(side=tk.LEFT)
        self.buttonSalir = tk.Button(self.frameBotones, width = ancho, height = 20,
                           text="SALIR", 
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra),
                           command=self.btSalir)
        self.buttonSalir.pack(side=tk.LEFT)
        
        return

    #def btConectar(self):
        
    #    #self.model.onConecta()
       
    #    return
    
    
    def btIngresar(self):
        
        #self.modificarEstado(self.estado.get())
        self.modificarEstado(self.estadoStr)
        
        monto = self.scrolledMonto.get("1.0", tk.END)
        self.model.onFondear(monto)
        self.scrolledMonto.delete("0.0", tk.END)
       
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
    
    
    #def btFondear(self):
    #    
    #    monto = self.scrolledMonto.get("1.0", tk.END)
    #    self.model.onFondear(monto)
    #    self.scrolledMonto.delete("0.0", tk.END)
       
    #    return
    
    
    def btApostar(self):
        
        monto = self.scrolledMonto.get("1.0", tk.END)
        self.model.onApostar(monto)
        self.scrolledMonto.delete("0.0", tk.END)
       
        return
    
    
    def btDoblar(self):
        
        self.model.onDoblar()
       
        return    

    
    def btSalir(self):
        
        #self.model.onSalir()
        self.root.quit()
        os._exit(0)
       
        return    

    
    def enviarMensaje(self):
        
        mensaje = self.entryEnvioMensajes.get("1.0", tk.END)
        self.entryEnvioMensajes.delete("0.0", tk.END)
        self.model.onEnviarMensaje(mensaje)
                
        return


    def inicializarEnvioMensajes(self):
      
        self.entryEnvioMensajes = ScrolledText(self.frameMenuEntry, 
                                    font=("Arial Bold", 10))
        self.entryEnvioMensajes.bind('<Return>', self.procesarMensaje)
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

    
    #def modificarUsuario(self, usuario):
        
    #    self.usuario.set("[" + usuario + "]")
        
    #    return
    
    
    #def cargarUsuario(self, usuario):
        
    #    self.modificarUsuario(usuario)
    #    self.labelUsuario = tk.Label(self.frameNombreUsuario, textvariable=self.usuario, 
    #                               font=("Arial Bold", 20), bg="medium blue", fg="white")
    #    self.labelUsuario.pack(side=tk.LEFT)

    #    return


    def modificarEstado(self, estado):
        
        self.usuario = self.model.MiNombre
        self.estadoStr = estado.replace('[', '').replace(']', '')
        self.estado.set(self.usuario + " "  + "$" + str(self.model.MiSaldo) + " (" + self.estadoStr + ")")
        self.modificarScore(self.model.MiPuntaje)
        self.cargarCartas(self.model.MisCartas)
        
        return
        
    
    def cargarEstado(self, estado):
        
        self.modificarEstado(estado)
        self.labelEstados = tk.Label(self.frameEstadoUsuario, textvariable=self.estado, 
                                   font=("Arial Bold", 25), bg="medium blue", fg="white")
        self.labelEstados.pack(side=tk.LEFT)

        return


    def modificarJugadores(self, jugadores):
        
        #self.jugadores.set(jugadores)
        self.textJugadores.delete("0.0", tk.END)
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


    def procesarMensaje(self, monto):
        
        if self.botonesActivados['mensaje']:
            self.enviarMensaje()

    
    def modificarMensajes(self, mensajes):
        
        #self.mensajes.set(mensajes)
        self.textChat.insert(tk.END, mensajes + "\n")
        self.textChat.see(tk.END)
        
        return
        
    
    def cargarMensajes(self, mensajes):

        self.scrollbarChat = tk.Scrollbar(self.frameChat) 
        self.textChat = tk.Text(self.frameChat, width=388, height=449,
                                font=("Arial Bold", 13), fg="blue", bg="white")
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


def testPantallaEjemplos(self):
    
    self.cartas = ['1-3', '2-4', '3-5', '4-2', '1-4', '2-2', '1-3', '2-4', '3-5', '4-2', '1-4', '2-2', '1-3', '2-4', '3-5', '4-2', '1-4', '2-2']
    self.cargarCartas(self.cartas)
    #self.modificarScore("20")
    self.modificarScore("20")
    self.modificarEstado("Plantado")
    self.modificarJugadores("Quique: Esperando\nSeba: Esperando\nFede G: Jugando\nFede F: Perdio\nRichard: Esperando")
    self.modificarMensajes("Seba: Esperando...\nQuique: me abuurroonnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn....")
    
    self.model.onPedirCarta()
    print("Test")
    self.mostrar()


def testPantallaPedirCarta():
    print("hola carta")


def testPantallaInicializador2():
    #cartas1 = ['1-3', '2-4', '3-5']
    listaCartas = ['1-3', '2-4', '3-5', '4-2', '1-4', '2-2']
    
    
    model = GuiViewModel()
    model.ee.on("pedirCartaEvent", testPantallaPedirCarta)
    
    bjScreen = PantallaPrincipal(model, "quique")
    bjScreen.cargarCartas(listaCartas)
    bjScreen.cargarScore("12")
    bjScreen.cargarEstado("Jug")
    #bjScreen.cargarUsuario("quique")
    bjScreen.cargarJugadores("Quique: Esperando\nSeba: Esperando\nFede G: Esperando\nFede F: Jugando\nRichard: Esperando")
    bjScreen.cargarMensajes("Quique: Esperando...\n")
    listaCartas = ['1_3', '2_4', '3_5']
    bjScreen.mostrar()
    
    test=input("prueba")
    

def testPantallaInicializador():
    #cartas1 = ['1-3', '2-4', '3-5']
    listaCartas = []
    model = GuiViewModel()
    model.MiSaldo = 3000
    model.ee.on("pedirCartaEvent", testPantallaPedirCarta)
    bjScreen = PantallaPrincipal(model, "quique")
    bjScreen.modificarEstado("Jugar")
    bjScreen.modificarScore("12")
    bjScreen.mostrar()

    '''    
    bjScreen.cargarCartas(listaCartas)
    bjScreen.cargarScore("12")
    bjScreen.cargarEstado("Jugar")
    bjScreen.cargarJugadores("Quique: Esperando\nSeba: Esperando\nFede G: Esperando\nFede F: Jugando\nRichard: Esperando")
    bjScreen.cargarMensajes("Quique: Esperando...\n")
    bjScreen.mostrar()
    
    test=input("prueba")
    '''


if __name__ == "__main__":

    testPantallaInicializador()
    
    