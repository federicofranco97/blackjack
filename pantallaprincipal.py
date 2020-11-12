import json
#import mkTkinter as tk
from mttkinter import mtTkinter as tk
import os
import playsound
from PIL import Image, ImageTk
import cbQueue
from guiViewModel import GuiViewModel
from tkinter.scrolledtext import ScrolledText
from _thread import *

from pantallautil import PantallaImagenes
from pantallautil import PantallaBase


class PantallaPrincipal:

    def __init__(self, model, tkroot):

        self.dobleroot = tkroot
        self.root = tk.Toplevel(self.dobleroot)

        self.lenguaje = "es"
        self.diccionario = {}
        self.cartas = []
        self.cartasBanca = []
        self.nombreJugador = tk.StringVar()
        self.scoreJugador = tk.StringVar()
        self.scoreBanca = tk.StringVar()
        self.usuario = model.MiNombre
        self.nombreJugador.set(self.usuario)
        self.estado = tk.StringVar()
        self.estadoStr = ""
        self.jugadores = tk.StringVar()
        self.mensajes = tk.StringVar()
        self.app = None
        self.labelScoreJugador = None
        self.labelScoreBanca = None
        self.model = model
        self.textChat = None
        
        self.cambiarIdioma('es')
        self.inicializarFrames()
        self.inicializarBotones()
        self.inicializarEnvioMensajes()  
        self.cargarScoreJugador("0")
        self.cargarScoreBanca("0")
        self.cargarEstado("...")
        self.cargarJugadores("")
        self.cargarBotones("")
        self.habilitarBotones()
        self.cargarMensajes("")
        
        self.configurarEventos()
        self.scrolledMonto.focus()
        
        return

    def cambiarIdioma(self, idioma):
        with open(os.path.join("lenguaje", idioma + ".py")) as json_file:
            self.diccionario = json.load(json_file)

    def cambioTurno(self, usuario):
        if usuario == self.usuario:
            start_new_thread(self.play, ())
        return
    
    def pIngresar(self):
        start_new_thread(self.playIngresar, ())

        return
    
    def pPierde(self):
        start_new_thread(self.playPierde, ())

        return
    
    def pEmpata(self):
        start_new_thread(self.playEmpata, ())

        return

    def pGana(self):
        start_new_thread(self.playGana, ())

        return

    def play(self):
        soundurl = os.path.join("sounds", "myTurn.mp3")
        playsound.playsound(soundurl)
        return


    def playIngresar(self):
        soundurl = os.path.join("sounds", "apostar.mp3")
        playsound.playsound(soundurl)
        return

    def playPierde(self):
        soundurl = os.path.join("sounds", "pierde.mp3")
        playsound.playsound(soundurl)
        return


    def playEmpata(self):
        soundurl = os.path.join("sounds", "empata.mp3")
        playsound.playsound(soundurl)
        return


    def playGana(self):
        soundurl = os.path.join("sounds", "gana.mp3")
        playsound.playsound(soundurl)
        return


    def configurarEventos(self):

        self.model.ee.on("refreshButtonsEvent", self.cargarBotones)
        self.model.ee.on("turnoChangedEvent", self.cambioTurno)
        self.model.ee.on("mensajeEntranteEvent", self.modificarMensajes)
        self.model.ee.on("estadoChangedEvent", self.modificarEstado)
        self.model.ee.on("juegoComenzadoEvent", self.juegoComenzado)
        self.model.ee.on("juegoTerminadoEvent", self.juegoTerminado)
        self.model.ee.on("jugadoresRefreshedEvent", self.modificarJugadores)
        self.model.ee.on("puntajeBancaChangedEvent", self.modificarScoreBanca)        

        return
    
    
    def modoEspera(self):
        
        return


    def inicializarFrames(self):
        
        #https://www.tutorialspoint.com/python/tk_button.htm
        self.root.wm_title("Blackjac UB version Betal Alfa Centauri v1.0.1")
        self.root.geometry("1024x768")
        self.root['bg']='medium blue'
 

        self.framePanelSuperior = tk.Frame(self.root, width = 1024, height = 718)
        self.framePanelSuperior.pack(side=tk.TOP)
        self.framePanelSuperior['bg']='medium blue'

        self.framePanelInferior = tk.Frame(self.root, width = 1024, height = 50)
        self.framePanelInferior.pack(side=tk.BOTTOM)
        self.framePanelInferior['bg']='medium blue'


        self.frameBotones = tk.Frame(self.framePanelSuperior, width = 1024, height = 30)
        self.frameBotones.pack(side=tk.TOP)
        self.frameBotones['bg']='medium blue'
        self.frameBotones.pack_propagate(0) 
        

        self.framePanel = tk.Frame(self.framePanelSuperior, width = 1024, height = 668)
        self.framePanel.pack(side=tk.BOTTOM)
        self.framePanel['bg']='medium blue'
        
 
        self.frameTablero = tk.Frame(self.framePanel, width = 624, height = 668)
        self.frameTablero.pack(side=tk.LEFT)
        self.frameTablero['bg']='medium blue'

        self.frameInfo = tk.Frame(self.framePanel, width = 400, height = 668)
        self.frameInfo.pack(side=tk.RIGHT)
        self.frameInfo['bg']='medium blue'       

        self.frameJuego = tk.Frame(self.frameTablero, width = 624, height = 518)
        self.frameJuego.pack(side=tk.TOP)
        self.frameJuego['bg']='medium blue'
        

        self.framePanelCartas = tk.Frame(self.frameJuego, width = 624, height = 468)
        self.framePanelCartas.pack(side=tk.TOP)
        self.framePanelCartas['bg']='green'
        self.framePanelCartas.pack_propagate(0)      


        self.frameCartasTitulo = tk.Frame(self.framePanelCartas, width = 624, height = 30)
        self.frameCartasTitulo.pack(side=tk.TOP)
        self.frameCartasTitulo['bg']='green'
        self.frameCartasTitulo.pack_propagate(0)      

        self.frameCartas = tk.Frame(self.framePanelCartas, width = 624, height = 438)
        self.frameCartas.pack(side=tk.BOTTOM)
        self.frameCartas['bg']='green'
        self.frameCartas.pack_propagate(0)


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
        self.frameInfoAuxiliar['bg']='medium blue'

        self.frameInfoDatos = tk.Frame(self.frameInfo, width = 398, height = 668)
        self.frameInfoDatos.pack(side=tk.RIGHT)
        self.frameInfoDatos['bg']='medium blue'

        self.frameScoreContexto = tk.Frame(self.frameInfoDatos, width = 398, height = 150)
        self.frameScoreContexto.pack(side=tk.TOP)
        self.frameScoreContexto['bg']='medium blue'
        
        self.frameScoreSeccion = tk.Frame(self.frameScoreContexto, width = 398, height = 148)
        self.frameScoreSeccion.pack(side=tk.TOP)
        self.frameScoreSeccion['bg']='medium blue'

        self.frameScoreSeparador = tk.Frame(self.frameScoreContexto, width = 398, height = 2)
        self.frameScoreSeparador.pack(side=tk.BOTTOM)
        self.frameScoreSeparador['bg']='medium blue'

        self.frameScorePanelJugador = tk.Frame(self.frameScoreSeccion, width = 164, height = 148)
        self.frameScorePanelJugador.pack(side=tk.LEFT)
        self.frameScorePanelJugador['bg']='medium blue'

        self.frameScorePanelOponente = tk.Frame(self.frameScoreSeccion, width = 234, height = 148)
        self.frameScorePanelOponente.pack(side=tk.RIGHT)
        self.frameScorePanelOponente['bg']='medium blue'


        self.frameScorePanelVS = tk.Frame(self.frameScorePanelOponente, width = 70, height = 148)
        self.frameScorePanelVS.pack(side=tk.LEFT)
        self.frameScorePanelVS['bg']='medium blue'

        self.frameScorePanelBanca = tk.Frame(self.frameScorePanelOponente, width = 164, height = 148)
        self.frameScorePanelBanca.pack(side=tk.RIGHT)
        self.frameScorePanelBanca['bg']='medium blue'


        self.frameScoreTituloJugador = tk.Frame(self.frameScorePanelJugador, width = 164, height = 30)
        self.frameScoreTituloJugador.pack(side=tk.TOP)
        self.frameScoreTituloJugador['bg']='medium blue'

        self.frameScorePuntajeJugador = tk.Frame(self.frameScorePanelJugador, width = 164, height = 118)
        self.frameScorePuntajeJugador.pack(side=tk.TOP)
        self.frameScorePuntajeJugador['bg']='medium blue'


        self.frameScoreTituloBanca = tk.Frame(self.frameScorePanelBanca, width = 164, height = 30)
        self.frameScoreTituloBanca.pack(side=tk.TOP)
        self.frameScoreTituloBanca['bg']='medium blue'

        self.frameScorePuntajeBanca = tk.Frame(self.frameScorePanelBanca, width = 164, height = 118)
        self.frameScorePuntajeBanca.pack(side=tk.BOTTOM)
        self.frameScorePuntajeBanca['bg']='medium blue'

        
        self.frameMenuChat = tk.Frame(self.frameInfoDatos, width = 390, height = 498)
        self.frameMenuChat.pack(side=tk.BOTTOM)
        self.frameMenuChat['bg']='white'
        self.frameMenuChat.pack_propagate(0)

        self.frameChat = tk.Frame(self.frameMenuChat, width = 390, height = 440)
        self.frameChat.pack(side=tk.TOP)
        self.frameChat['bg']='white'
        self.frameChat.pack_propagate(0)
        

        self.frameChatPanelServidor = tk.Frame(self.frameChat, width = 390, height = 220)
        self.frameChatPanelServidor.pack(side=tk.TOP)
        self.frameChatPanelServidor['bg']='white'
        self.frameChatPanelServidor.pack_propagate(0)

        self.frameChatPanelMensajes = tk.Frame(self.frameChat, width = 390, height = 220)
        self.frameChatPanelMensajes.pack(side=tk.BOTTOM)
        self.frameChatPanelMensajes['bg']='white'
        self.frameChatPanelMensajes.pack_propagate(0)
        
                
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
        
        self.botones = self.model.Acciones
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
            if (boton == 'ingresar' or boton == 'apostar') and self.botonesActivados[boton]:
                self.pIngresar()
        
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
        
        if self.botonesActivados['ingresar']:
            self.btIngresar()
        elif self.botonesActivados['apostar']:
            self.btApostar()


    def inicializarBotones(self):

        ancho = 12
        colorFront = "white"
        colorBack = "medium blue"
        tamLetra = 13
        tamMonto = 15
 
        self.buttonIngresar = tk.Button(self.frameBotones, width = ancho, height = 20, 
                           text=self.diccionario["ingresar"],
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra, "bold"),
                           command=self.btIngresar)
        self.buttonIngresar.pack(side=tk.LEFT)
        self.labelPesos = tk.Label(self.frameBotones, text="$",width = 1, height = 20,
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra, "bold"))
        self.labelPesos.pack(side=tk.LEFT)
        self.scrolledMonto = tk.Text(self.frameBotones, width = 10, height = 18, 
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamMonto, "bold"))
        self.scrolledMonto.bind('<Return>', self.procesarMonto)
        self.scrolledMonto.pack(side=tk.LEFT)
        self.buttonApostar = tk.Button(self.frameBotones, width = ancho, height = 20,
                           text=self.diccionario["apostar"],
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra, "bold"),
                           command=self.btApostar)
        self.buttonApostar.pack(side=tk.LEFT)
        self.buttonPedir = tk.Button(self.frameBotones, width = ancho, height = 20,
                           text=self.diccionario["pedir"],
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra, "bold"),
                           command=self.btPedir)
        self.buttonPedir.pack(side=tk.LEFT)
        self.buttonPlantarse = tk.Button(self.frameBotones, width = ancho, height = 20,
                           text=self.diccionario["plantarse"],
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra, "bold"),
                           command=self.btPlantarse)
        self.buttonPlantarse.pack(side=tk.LEFT)
        self.buttonSeparar = tk.Button(self.frameBotones, width = ancho, height = 20,
                           text=self.diccionario["separar"],
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra, "bold"),
                           command=self.btSeparar)
        self.buttonSeparar.pack(side=tk.LEFT)
        self.buttonDoblar = tk.Button(self.frameBotones, width = ancho, height = 20,
                           text=self.diccionario["doblar"],
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra, "bold"),
                           command=self.btDoblar)
        self.buttonDoblar.pack(side=tk.LEFT)
        self.buttonSalir = tk.Button(self.frameBotones, width = ancho, height = 20,
                           text=self.diccionario["salir"],
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra, "bold"),
                           command=self.btSalir)
        self.buttonSalir.pack(side=tk.LEFT)
        
        return


    def limpiarTablero(self):
        
        for widget in self.frameCartas.winfo_children():
            widget.destroy()

        return

    def isValidStr(self, cadena, filtro):
        
        for caracter in cadena:
            if caracter not in filtro:
                return False
            
        return True


    def btIngresar(self):
        
        self.modificarEstado(self.estadoStr)
        
        monto = self.scrolledMonto.get("1.0", tk.END).replace("\n","")
        if self.isValidStr(monto, list("0123456789".strip())) and len(monto) <= 10:
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


    def btApostar(self):

        monto = self.scrolledMonto.get("1.0", tk.END)
        self.model.onApostar(monto)
        self.scrolledMonto.delete("0.0", tk.END)
        return
    
    
    def btDoblar(self):
        self.model.onDoblar()
        return    

    
    def btSalir(self):
        self.root.quit()
        os._exit(0)
        return    

    
    def enviarMensaje(self):
        mensaje = self.entryEnvioMensajes.get("1.0", tk.END)
        self.entryEnvioMensajes.delete("0.0", tk.END)
        self.model.onEnviarMensaje(mensaje)
        
        return


    def inicializarEnvioMensajes(self):
        self.entryEnvioMensajes = ScrolledText(self.frameMenuEntry, font=("Arial Bold", 10))
        self.entryEnvioMensajes.bind('<Return>', self.procesarMensaje)
        self.entryEnvioMensajes.pack()

        self.buttonEnviarMensaje = tk.Button(self.frameMenuButton, width = 48, height = 48,
                           text=self.diccionario["enviar"],
                           fg="white",
                           bg="medium blue",
                           command=self.enviarMensaje)
        self.buttonEnviarMensaje.pack()
        
        return


    def modificarScoreJugador(self, score):
        
        self.scoreJugadorStr = score
        self.scoreJugador.set(score)
        
        return
        

    def modificarScoreBanca(self, puntaje, cartas):

        self.scoreBancaStr = puntaje
        self.scoreBanca.set(puntaje)
        self.cartasBanca = cartas
            
        return

    
    def cargarScoreJugador(self, score):
        
        self.modificarScoreJugador(score)
        self.labelTituloJugador = tk.Label(self.frameScoreTituloJugador, textvariable=self.nombreJugador, 
                                   font=("Arial Bold", 20, "bold"), bg="medium blue", fg="white")
        self.labelTituloJugador.pack(side=tk.TOP)
        self.labelScoreJugador = tk.Label(self.frameScorePuntajeJugador, textvariable=self.scoreJugador, 
                                   font=("Arial Bold", 80, "bold"), bg="medium blue", fg="white")
        self.labelScoreJugador.pack(side=tk.BOTTOM)

        return

    
    def cargarScoreBanca(self, score):
        
        self.modificarScoreBanca(score, [])
        self.labelTituloVS = tk.Label(self.frameScorePanelVS, text=" - ", 
                                   font=("Arial Bold", 80, "bold"), bg="medium blue", fg="white")
        self.labelTituloVS.pack(side=tk.TOP)
        self.labelTituloBanca = tk.Label(self.frameScoreTituloBanca, text="BANCA", 
                                   font=("Arial Bold", 20, "bold"), bg="medium blue", fg="white")
        self.labelTituloBanca.pack(side=tk.TOP)
        self.labelScoreBanca = tk.Label(self.frameScorePuntajeBanca, textvariable=self.scoreBanca, 
                                   font=("Arial Bold", 80, "bold"), bg="medium blue", fg="white")
        self.labelScoreBanca.pack(side=tk.BOTTOM)

        return


    def juegoTerminado(self):
        
        scoreBanca = self.scoreBanca
        scoreJugador = self.scoreJugador
        
        estado = ""
        if self.estadoStr == "finalizado_perdido":
            estado = " (PERDISTE)"
        elif self.estadoStr == "finalizado_empate":
            estado = " (EMPATASTE)"
        elif self.estadoStr == "finalizado_ganador":
            estado = " (GANASTE)"

        estadoBanca = "BANCA: " + str(self.scoreBancaStr)
        estadoJugador = self.usuario + ": " + str(self.scoreJugadorStr) + estado
        
        y0 = 230
        if len(self.cartas) > 7:
            y0 = y0 + 60
            
        self.cargarCartas(self.cartasBanca, reducir=True, borrar=True, x0=100, y0=0)
        self.cargarCartas(self.cartas     , reducir=True,              x0=100, y0=200)
        
        for widget in self.frameCartasTitulo.winfo_children():
            widget.destroy()
        self.labelTerminadoBanca = tk.Label(self.frameCartasTitulo, text=estadoBanca, 
                                   font=("Arial Bold", 20, "bold"), bg="green", fg="yellow")
        self.labelTerminadoBanca.pack(side=tk.TOP)
        self.labelTerminadoJugador = tk.Label(self.frameCartas, text=estadoJugador, 
                                   font=("Arial Bold", 20, "bold"), bg="green", fg="yellow")
        self.labelTerminadoJugador.pack(side=tk.BOTTOM)

        #self.cargarCartas(self.cartasBanca, reducir=False, borrar=True, x0=20, y0=80)
        
        if self.estadoStr == "finalizado_perdido":
            self.pPierde()
        elif self.estadoStr == "finalizado_empate":
            self.pEmpata()
        elif self.estadoStr == "finalizado_ganador":
            self.pGana()
        
        return


    def juegoComenzado(self, mensaje):

        self.modificarMensajes("SERVIDOR", "\n\n" + "-------------------------\n" + "\n" + mensaje + "\n")
        self.limpiarTablero()
        self.scrolledMonto.focus()
        self.modificarEstado("")
        
        return

    def modificarEstado(self, estado):
        
        self.usuario = self.model.MiNombre
        self.estadoStr = estado.replace('[', '').replace(']', '')
        self.estado.set(self.usuario + " " + "$" + str(self.model.MiSaldo) + " (" + self.estadoStr + ")")
        self.modificarScoreJugador(self.model.MiPuntaje)
        cartas = self.model.MisCartas
        
        if len(self.cartas) != len(cartas):
            for widget in self.frameCartasTitulo.winfo_children():
                widget.destroy()
            self.cargarCartas([], borrar=True, comparar=False, x0=20, y0=120)
            self.labelTerminadoBanca = tk.Label(self.frameCartasTitulo, text="BANCA    ", 
                               font=("Arial Bold", 20, "bold"), bg="green", fg="yellow")
            self.labelTerminadoBanca.pack(side=tk.RIGHT)
            self.cargarCartas(cartas, borrar=False, comparar=False, x0=20, y0=120)
        else:
            self.cargarCartas(cartas, borrar=True, comparar=True, x0=20, y0=120)

        
        if len(cartas) > 0:
            listaCartas = [cartas[0], 'reverso']
            self.cargarCartas(listaCartas, reducir=True, borrar=False, x0=450, y0=0)

        self.cartas = cartas
        
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

    
    def modificarMensajes(self, mensajes, tipo):
        
        #self.mensajes.set(mensajes)
        if tipo == "SERVIDOR":
            self.textChatServidor.insert(tk.END, mensajes + "\n")
            self.textChatServidor.see(tk.END)
        elif tipo == "MENSAJE":
            self.textChatMensajes.insert(tk.END, mensajes + "\n")
            self.textChatMensajes.see(tk.END)
        
        return
        
    
    def cargarMensajes(self, mensajes):

        self.scrollbarChatServidor = tk.Scrollbar(self.frameChatPanelServidor) 
        self.textChatServidor = tk.Text(self.frameChatPanelServidor, width=388, height=200,
                                font=("Arial Bold", 12), fg="blue", bg="white")
        self.scrollbarChatServidor.pack(side=tk.RIGHT, fill=tk.Y)
        self.textChatServidor.pack(side=tk.LEFT, fill=tk.Y)
        self.scrollbarChatServidor.config(command=self.textChatServidor.yview)
        self.textChatServidor.config(yscrollcommand=self.scrollbarChatServidor.set)
        self.textChatServidor.pack(side=tk.LEFT)

        self.scrollbarChatMensajes = tk.Scrollbar(self.frameChatPanelMensajes) 
        self.textChatMensajes = tk.Text(self.frameChatPanelMensajes, width=388, height=200,
                                font=("Arial Bold", 12), fg="blue", bg="white")
        self.scrollbarChatMensajes.pack(side=tk.RIGHT, fill=tk.Y)
        self.textChatMensajes.pack(side=tk.LEFT, fill=tk.Y)
        self.scrollbarChatMensajes.config(command=self.textChatMensajes.yview)
        self.textChatMensajes.config(yscrollcommand=self.scrollbarChatMensajes.set)
        self.textChatMensajes.pack(side=tk.LEFT)

        #self.modificarMensajes(mensajes)
        
        return

    
    def cargarCartas(self, cartas, reducir=False, borrar=False, invertir=False, comparar=False, x0=0, y0=0):

        if len(cartas) == 0:
            print('no hay cartas')
            return

        if len(cartas) == len(self.cartas) and comparar:
            iguales = True
            for i in range(0, len(cartas)):
                if cartas[i] != self.cartas[i]:
                    print('cartas diferentes')
                    iguales = False
                    break
            
            if iguales == True:
                print('Ya se estan mostrando esas cartas')
                return
            
        print('Tengo cartas')
        print(cartas)
        #self.cartas = cartas
        
        if self.app == None:
            self.app = PantallaImagenes(self.frameCartas)
            self.app['bg']='green'
        else:
            if borrar:
                self.app.borrar()
        
        self.cwd = os.getcwd()
        mazo = 'mazo'
        self.imgList = []
        #x0 = 20
        #y0 = 5
        xOffset = 60
        yOffset = 5
        yLineOffset = 60
        factorInversion = 1
        if invertir:
            factorInversion = -1
        cartasPorLinea = 7
        x = x0
        y = y0
        if len(cartas) <= cartasPorLinea and y0 >= 100:
            y = y + yLineOffset
        for i in range(0, len(cartas)):
            
            self.imgList.append(os.path.join(os.path.join(self.cwd, mazo), cartas[i] + '.jpg'))
            #self.imgList.append(os.path.join(os.path.join(self.cwd, mazo), self.cartas[i] + '.jpg'))
            if reducir:
                self.app.agregar(self.imgList[i], x=x, y=y, width = 90, height = 126)
                #self.app.agregar(self.imgList[i], x=x, y=y, width = 135, height = 189)
            else:
                self.app.agregar(self.imgList[i], x=x, y=y, width = 158, height = 221)

            x = x + xOffset * factorInversion 
            y = y + yOffset 
            if (i+1) % cartasPorLinea == 0:
                x = x0
                y = y0 + int((i/cartasPorLinea)*yLineOffset)
 
        return


def testPantallaPedirCarta():
    print("hola carta")


def testPantallaInicializador():
    cartas1 = ['1-3', '2-4', '3-5']
    cartas2 = ['1-3', '2-4', '3-5', '1-3', '2-4', '3-5']
    cartas = ['1-3', '2-4', '3-5', '4-2', '1-4', '2-2', '1-3', '2-4', '3-5', '4-2', '1-4', '2-2', '1-3', '2-4']
    listaCartas = []
    model = GuiViewModel()
    model.MiSaldo = 3000
    model.MisCartas = cartas
    model.MiNombre = "test"

    model.ee.on("pedirCartaEvent", testPantallaPedirCarta)
    bjbase = PantallaBase()
    bjScreen = PantallaPrincipal(model, bjbase.getRoot())
    bjScreen.cartasBanca = ['4-2', '1-4', '2-2']
    bjScreen.usuario = "test"
    bjScreen.scoreBancaStr = "12"
    bjScreen.scoreJugadorStr = "12"
    bjScreen.modificarScoreJugador("12")
    bjScreen.modificarScoreBanca("12", cartas)
    bjScreen.modificarEstado("Jugar")
    #bjScreen.juegoTerminado()
    #668-90-20, 20
    #20, 320
    bjScreen.mostrar()

    '''    
    bjScreen.cargarCartas(listaCartas)
    bjScreen.cargarScoreJugador("12")
    bjScreen.cargarEstado("Jugar")
    bjScreen.cargarJugadores("Quique: Esperando\nSeba: Esperando\nFede G: Esperando\nFede F: Jugando\nRichard: Esperando")
    bjScreen.cargarMensajes("Quique: Esperando...\n")
    bjScreen.mostrar()
    
    test=input("prueba")
    '''


if __name__ == "__main__":

    testPantallaInicializador()
    
    