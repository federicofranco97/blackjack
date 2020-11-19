import json
import os
import playsound
from mttkinter import mtTkinter as tk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
from _thread import *

from guiViewModel import GuiViewModel
from pantallautil import PantallaImagenes
from pantallautil import PantallaBase

class PantallaPrincipal:
    '''
    Clase: PantallaPrincipal
        
    Descripcion: Presenta la pantalla princiapl del juego y permite la interaccion
                 del usuario. 
    '''


    def __init__(self, model, tkroot):
        '''
        Metodo: __init__
        
        Parametros: model: Clase GuiViewModel para intercambio de informacion y comunicacion 
                           entre el cliente y la clase PantallaPrincipal. 
                    tkroot: Frame Root al que pertenece la ventana
        
        Descripcion: Constructor de la clase, inicializa y prepara la ventana para ser mostrada 
        '''

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
        self.jugadoresStr = ""
        self.jugadores = tk.StringVar()
        self.mensajes = tk.StringVar()
        self.app = None
        self.labelScoreJugador = None
        self.labelScoreBanca = None
        self.model = model
        self.textChat = None
        self.comenzado = False
        self.cartasBancaEnPantalla = False
        
        self.cambiarIdioma('es')

        self.statJugadores = tk.StringVar()
        self.stat = tk.StringVar()
        
        self.inicializarFrames()
        self.crearMenu()
        self.crearMenuEnvioMensajes()  
        self.crearMenuScoreJugador("0")
        self.crearMenuScoreBanca("0")
        self.crearEstado("...")
        self.crearJugadores("")
        self.cargarBotones("")
        self.habilitarBotones()
        self.crearMenuMensajes("")

        self.textoBotonStatJugadores = self.diccionario["stats"]
        
        self.configurarEventos()
        self.scrolledMonto.focus()
        
        return


    def cambiarIdioma(self, idioma):
        '''
        Metodo: cambiarIdioma
        
        Parametros: idioma: Idioma a configurar. 
        
        Descripcion: Permite cambiar el idioma de los mensajes del juego.
        
        Retorno: No retorna ningun valor. 
        '''
        
        with open(os.path.join("lenguaje", idioma + ".py")) as json_file:
            self.diccionario = json.load(json_file)
        
        return


    def cambioTurno(self, usuario):
        '''
        Metodo: cambioTurno
        
        Parametros: usuario: Usuario con turno activo que puede jugar. 
        
        Descripcion: Si le corresponde el turno al usuario Lanza la reproduccion del audio de Juego.
        
        Retorno: No retorna ningun valor. 
        '''
        
        if usuario == self.usuario:
            start_new_thread(self.playTurno, ())

        return
    
    
    def pIngresar(self):
        '''
        Metodo: pIngresar
        
        Parametros: No tiene parametros. 
        
        Descripcion: Lanza la reproduccion del audio para Ingresor/Apostar dinero
        
        Retorno: No retorna ningun valor. 
        '''
        
        start_new_thread(self.playIngresar, ())

        return

    
    def pPierde(self):
        '''
        Metodo: pPierde
        
        Parametros: No tiene parametros. 
        
        Descripcion: Lanza la reproduccion del audio para Perdedor
        
        Retorno: No retorna ningun valor. 
        '''

        start_new_thread(self.playPierde, ())

        return
    
    
    def pEmpata(self):
        '''
        Metodo: pEmpata
        
        Parametros: No tiene parametros. 
        
        Descripcion: Lanza la reproduccion del audio para Empate
        
        Retorno: No retorna ningun valor. 
        '''

        start_new_thread(self.playEmpata, ())

        return


    def pGana(self):
        '''
        Metodo: pGana
        
        Parametros: No tiene parametros. 
        
        Descripcion: Lanza la reproduccion del audio para Ganador
        
        Retorno: No retorna ningun valor. 
        '''

        start_new_thread(self.playGana, ())

        return


    def playTurno(self):
        '''
        Metodo: playTurno
        
        Parametros: No tiene parametros. 
        
        Descripcion: Reproduce el audio de usuario con Turno activo
        
        Retorno: No retorna ningun valor. 
        '''

        soundurl = os.path.join("sounds", "myTurn.mp3")
        try:
            playsound.playsound(soundurl)
        except playsound.PlaysoundException:
            error = 1

        return


    def playIngresar(self):
        '''
        Metodo: playIngresar
        
        Parametros: No tiene parametros. 
        
        Descripcion: Reproduce el audio de usuario puede Ingresar dinero o Apostar
        
        Retorno: No retorna ningun valor. 
        '''

        soundurl = os.path.join("sounds", "apostar.mp3")
        try:
            playsound.playsound(soundurl)
        except playsound.PlaysoundException:
            error = 1

        return

    def playPierde(self):
        '''
        Metodo: playPierde
        
        Parametros: No tiene parametros. 
        
        Descripcion: Reproduce el audio usuario que pierde
        
        Retorno: No retorna ningun valor. 
        '''

        soundurl = os.path.join("sounds", "pierde.mp3")
        try:
            playsound.playsound(soundurl)
        except playsound.PlaysoundException:
            error = 1

        return


    def playEmpata(self):
        '''
        Metodo: playEmpata
        
        Parametros: No tiene parametros. 
        
        Descripcion: Reproduce el audio usuario que empata
        
        Retorno: No retorna ningun valor. 
        '''

        soundurl = os.path.join("sounds", "empata.mp3")
        try:
            playsound.playsound(soundurl)
        except playsound.PlaysoundException:
            error = 1

        return


    def playGana(self):
        '''
        Metodo: playGana
        
        Parametros: No tiene parametros. 
        
        Descripcion: Reproduce el audio usuario que gana
        
        Retorno: No retorna ningun valor. 
        '''

        soundurl = os.path.join("sounds", "gana.mp3")
        try:
            playsound.playsound(soundurl)
        except playsound.PlaysoundException:
            error = 1

        return


    def configurarEventos(self):
        '''
        Metodo: configurarEventos
        
        Parametros: No tiene parametros. 
        
        Descripcion: Activa los callbacks para manejar los eventos que se reciben del 
                    thread del cliente.
        
        Retorno: No retorna ningun valor. 
        '''

        self.model.ee.on("refreshButtonsEvent", self.cargarBotones)
        self.model.ee.on("turnoChangedEvent", self.cambioTurno)
        self.model.ee.on("mensajeEntranteEvent", self.cbModificarMensajes)
        self.model.ee.on("estadoChangedEvent", self.cbModificarEstado)
        self.model.ee.on("juegoComenzadoEvent", self.cbJuegoComenzado)
        self.model.ee.on("juegoTerminadoEvent", self.cbJuegoTerminado)
        self.model.ee.on("jugadoresRefreshedEvent", self.cbModificarJugadores)
        self.model.ee.on("puntajeBancaChangedEvent", self.modificarScoreBanca)
        self.model.ee.on("estadisticasRecibidasEvent", self.cbEstadisticasRecibidas)

        return
    
    
    def inicializarFrames(self):
        '''
        Metodo: inicializarFrames
        
        Parametros: No tiene parametros. 
        
        Descripcion: Crea todos los frames de la Pantalla Principal para ubicar los objetos
                     (botones, labels, texts, etc) y poder presentar el juego.
        
        Retorno: No retorna ningun valor. 
        '''

        # Configura Titulo de ventana
        self.root.wm_title("Blackjac UB v1.0")
        self.root.geometry("1024x768")
        self.root['bg']='medium blue'
 
        # Creacion de frames
 
        ''' framePanelSuperior: Nivel 1 - Frame Padre: root - Posicion: TOP'''
        self.framePanelSuperior = tk.Frame(self.root, width = 1024, height = 718)
        self.framePanelSuperior.pack(side=tk.TOP)
        self.framePanelSuperior['bg']='medium blue'
 
        ''' framePanelInferior: Nivel 2 - Frame Padre: root - Posicion: BOTTOM'''
        self.framePanelInferior = tk.Frame(self.root, width = 1024, height = 50)
        self.framePanelInferior.pack(side=tk.BOTTOM)
        self.framePanelInferior['bg']='medium blue'


        ''' frameBotones: Nivel 1.1 - Frame Padre: framePanelSuperior - Posicion: TOP'''
        self.frameBotones = tk.Frame(self.framePanelSuperior, width = 1024, height = 30)
        self.frameBotones.pack(side=tk.TOP)
        self.frameBotones['bg']='medium blue'
        self.frameBotones.pack_propagate(0) 
        
        ''' framePanel: Nivel 1.2 - Frame Padre: framePanelSuperior - Posicion: BOTTOM'''
        self.framePanel = tk.Frame(self.framePanelSuperior, width = 1024, height = 668)
        self.framePanel.pack(side=tk.BOTTOM)
        self.framePanel['bg']='medium blue'
        
 
        ''' frameTablero: Nivel 1.2.1 - Frame Padre: framePanel - Posicion: LEFT'''
        self.frameTablero = tk.Frame(self.framePanel, width = 624, height = 668)
        self.frameTablero.pack(side=tk.LEFT)
        self.frameTablero['bg']='medium blue'

        ''' frameInfo: Frame 1.2.2 - Frame Padre: framePanel - Posicion: RIGHT'''
        self.frameInfo = tk.Frame(self.framePanel, width = 400, height = 668)
        self.frameInfo.pack(side=tk.RIGHT)
        self.frameInfo['bg']='medium blue'       


        ''' frameJuego: Frame 1.2.1.1 - Frame Padre: frameTablero - Posicion: TOP'''
        self.frameJuego = tk.Frame(self.frameTablero, width = 624, height = 518)
        self.frameJuego.pack(side=tk.TOP)
        self.frameJuego['bg']='medium blue'

        ''' frameJugadores: Frame 1.2.1.2 - Frame Padre: frameTablero - Posicion: BOTTOM'''
        self.frameJugadores = tk.Frame(self.frameTablero, width = 624, height = 150)
        self.frameJugadores.pack(side=tk.BOTTOM)
        self.frameJugadores['bg']='white'
        self.frameJugadores.pack_propagate(0)
        
        
        ''' frameJugadores: Frame 1.2.1.2.1 - Frame Padre: frameJugadores - Posicion: TOP'''
        self.frameJugadoresInformacion = tk.Frame(self.frameJugadores, width = 624, height = 75)
        self.frameJugadoresInformacion.pack(side=tk.TOP)
        self.frameJugadoresInformacion['bg']='white'
        self.frameJugadoresInformacion.pack_propagate(0)

        ''' frameJugadores: Frame 1.2.1.2.2 - Frame Padre: frameJugadores - Posicion: BOTTOM'''
        self.frameJugadoresEstadisticas = tk.Frame(self.frameJugadores, width = 624, height = 75)
        self.frameJugadoresEstadisticas.pack(side=tk.BOTTOM)
        self.frameJugadoresEstadisticas['bg']='white'
        self.frameJugadoresEstadisticas.pack_propagate(0)

        ''' framePanelCartas: Frame 1.2.1.1.1 - Frame Padre: frameJuego - Posicion: TOP'''
        self.framePanelCartas = tk.Frame(self.frameJuego, width = 624, height = 468)
        self.framePanelCartas.pack(side=tk.TOP)
        self.framePanelCartas['bg']='green'
        self.framePanelCartas.pack_propagate(0)      

        ''' frameEstadoUsuario: Frame 1.2.1.1.2 - Frame Padre: frameJuego - Posicion: BOTTOM'''
        self.frameEstadoUsuario = tk.Frame(self.frameJuego, width = 624, height = 50)
        self.frameEstadoUsuario.pack(side=tk.BOTTOM)
        self.frameEstadoUsuario['bg']='medium blue' 
        self.frameEstadoUsuario.pack_propagate(0)


        ''' frameCartasTitulo: Frame 1.2.1.1.1.1 - Frame Padre: framePanelCartas - Posicion: TOP'''
        self.frameCartasTitulo = tk.Frame(self.framePanelCartas, width = 624, height = 30)
        self.frameCartasTitulo.pack(side=tk.TOP)
        self.frameCartasTitulo['bg']='green'
        self.frameCartasTitulo.pack_propagate(0)      

        ''' frameCartas: Frame 1.2.1.1.1.1 - Frame Padre: framePanelCartas - Posicion: BOTTOM'''
        self.frameCartas = tk.Frame(self.framePanelCartas, width = 624, height = 438)
        self.frameCartas.pack(side=tk.BOTTOM)
        self.frameCartas['bg']='green'
        self.frameCartas.pack_propagate(0)


        ''' frameInfoAuxiliar: Frame 1.2.2.1 - Frame Padre: frameInfo - Posicion: LEFT'''
        self.frameInfoAuxiliar = tk.Frame(self.frameInfo, width = 2, height = 668)
        self.frameInfoAuxiliar.pack(side=tk.LEFT)
        self.frameInfoAuxiliar['bg']='medium blue'

        ''' frameInfoDatos: Frame 1.2.2.2 - Frame Padre: frameInfo - Posicion: RIGHT'''
        self.frameInfoDatos = tk.Frame(self.frameInfo, width = 398, height = 668)
        self.frameInfoDatos.pack(side=tk.RIGHT)
        self.frameInfoDatos['bg']='medium blue'


        ''' frameScoreContexto: Frame 1.2.2.2.1 - Frame Padre: frameInfoDatos - Posicion: TOP'''
        self.frameScoreContexto = tk.Frame(self.frameInfoDatos, width = 398, height = 150)
        self.frameScoreContexto.pack(side=tk.TOP)
        self.frameScoreContexto['bg']='medium blue'

        ''' frameScoreContexto: Frame 1.2.2.2.2 - Frame Padre: frameInfoDatos - Posicion: BOTTOM'''
        self.frameMenuChat = tk.Frame(self.frameInfoDatos, width = 390, height = 498)
        self.frameMenuChat.pack(side=tk.BOTTOM)
        self.frameMenuChat['bg']='white'
        self.frameMenuChat.pack_propagate(0)


        ''' frameScoreSeccion: Frame 1.2.2.2.1.1 - Frame Padre: frameScoreContexto - Posicion: TOP'''
        self.frameScoreSeccion = tk.Frame(self.frameScoreContexto, width = 398, height = 148)
        self.frameScoreSeccion.pack(side=tk.TOP)
        self.frameScoreSeccion['bg']='medium blue'

        ''' frameScoreSeparador: Frame 1.2.2.2.1.2 - Frame Padre: frameScoreContexto - Posicion: BOTTOM'''
        self.frameScoreSeparador = tk.Frame(self.frameScoreContexto, width = 398, height = 2)
        self.frameScoreSeparador.pack(side=tk.BOTTOM)
        self.frameScoreSeparador['bg']='medium blue'


        ''' frameScorePanelJugador: Frame 1.2.2.2.1.1.1 - Frame Padre: frameScoreSeccion - Posicion: LEFT'''
        self.frameScorePanelJugador = tk.Frame(self.frameScoreSeccion, width = 164, height = 148)
        self.frameScorePanelJugador.pack(side=tk.LEFT)
        self.frameScorePanelJugador['bg']='medium blue'

        ''' frameScorePanelOponente: Frame 1.2.2.2.1.1.2 - Frame Padre: frameScoreSeccion - Posicion: RIGHT'''
        self.frameScorePanelOponente = tk.Frame(self.frameScoreSeccion, width = 234, height = 148)
        self.frameScorePanelOponente.pack(side=tk.RIGHT)
        self.frameScorePanelOponente['bg']='medium blue'


        ''' frameScorePanelVS: Frame 1.2.2.2.1.1.2.1 - Frame Padre: frameScorePanelOponente - Posicion: LEFT'''
        self.frameScorePanelVS = tk.Frame(self.frameScorePanelOponente, width = 70, height = 148)
        self.frameScorePanelVS.pack(side=tk.LEFT)
        self.frameScorePanelVS['bg']='medium blue'

        ''' frameScorePanelBanca: Frame 1.2.2.2.1.1.2.2 - Frame Padre: frameScorePanelOponente - Posicion: RIGHT'''
        self.frameScorePanelBanca = tk.Frame(self.frameScorePanelOponente, width = 164, height = 148)
        self.frameScorePanelBanca.pack(side=tk.RIGHT)
        self.frameScorePanelBanca['bg']='medium blue'


        ''' frameScoreTituloJugador: Frame 1.2.2.2.1.1.1.1 - Frame Padre: frameScorePanelJugador - Posicion: TOP'''
        self.frameScoreTituloJugador = tk.Frame(self.frameScorePanelJugador, width = 164, height = 30)
        self.frameScoreTituloJugador.pack(side=tk.TOP)
        self.frameScoreTituloJugador['bg']='medium blue'

        '''frameScorePuntajeJugador: Frame 1.2.2.2.1.1.1.2 - Frame Padre: frameScorePanelJugador - Posicion: BOTTOM''' 
        self.frameScorePuntajeJugador = tk.Frame(self.frameScorePanelJugador, width = 164, height = 118)
        self.frameScorePuntajeJugador.pack(side=tk.BOTTOM)
        self.frameScorePuntajeJugador['bg']='medium blue'


        ''' frameScoreTituloBanca: Frame 1.2.2.2.1.1.2.2.1 - Frame Padre: frameScorePanelBanca - Posicion: TOP'''
        self.frameScoreTituloBanca = tk.Frame(self.frameScorePanelBanca, width = 164, height = 30)
        self.frameScoreTituloBanca.pack(side=tk.TOP)
        self.frameScoreTituloBanca['bg']='medium blue'

        ''' frameScorePuntajeBanca: Frame 1.2.2.2.1.1.2.2.2 - Frame Padre: frameScorePanelBanca - Posicion: BOTTOM'''
        self.frameScorePuntajeBanca = tk.Frame(self.frameScorePanelBanca, width = 164, height = 118)
        self.frameScorePuntajeBanca.pack(side=tk.BOTTOM)
        self.frameScorePuntajeBanca['bg']='medium blue'

        
        ''' frameChat: Frame 1.2.2.2.2.1 - Frame Padre: frameMenuChat - Posicion: TOP'''
        self.frameChat = tk.Frame(self.frameMenuChat, width = 390, height = 440)
        self.frameChat.pack(side=tk.TOP)
        self.frameChat['bg']='white'
        self.frameChat.pack_propagate(0)
        
        ''' frameMensaje: Frame 1.2.2.2.2.2 - Frame Padre: frameMenuChat - Posicion: BOTTOM'''
        self.frameMensaje = tk.Frame(self.frameMenuChat, width = 390, height = 60)
        self.frameMensaje.pack(side=tk.BOTTOM)
        self.frameMensaje['bg']='white'
        self.frameMensaje.pack_propagate(0)


        ''' frameChatPanelServidor: Frame 1.2.2.2.2.1.1 - Frame Padre: frameChat - Posicion: TOP'''
        self.frameChatPanelServidor = tk.Frame(self.frameChat, width = 390, height = 220)
        self.frameChatPanelServidor.pack(side=tk.TOP)
        self.frameChatPanelServidor['bg']='white'
        self.frameChatPanelServidor.pack_propagate(0)

        ''' frameChatPanelServidor: Frame 1.2.2.2.2.1.1 - Frame Padre: frameChat - Posicion: BOTTOM'''
        self.frameChatPanelMensajes = tk.Frame(self.frameChat, width = 390, height = 220)
        self.frameChatPanelMensajes.pack(side=tk.BOTTOM)
        self.frameChatPanelMensajes['bg']='white'
        self.frameChatPanelMensajes.pack_propagate(0)
        
                
        ''' frameMenuEntry: Frame 1.2.2.2.2.2.1 - Frame Padre: frameMensaje - Posicion: LEFT'''
        self.frameMenuEntry = tk.Frame(self.frameMensaje, width = 340, height = 60)
        self.frameMenuEntry.pack(side=tk.LEFT)
        self.frameMenuEntry['bg']='white'
        self.frameMenuEntry.pack_propagate(0)
        
        ''' frameMenuEntry: Frame 1.2.2.2.2.2.2 - Frame Padre: frameMensaje - Posicion: RIGHT'''
        self.frameMenuButton = tk.Frame(self.frameMensaje, width = 50, height = 60)
        self.frameMenuButton.pack(side=tk.RIGHT)
        self.frameMenuButton['bg']='white'
        self.frameMenuButton.pack_propagate(0)
                        
        return
            
    def cbEstadisticasRecibidas(self, estadisticas):
        '''
        Metodo: cbEstadisticasRecibidas
        
        Parametros: estadisticas: Datos de estadisticas recibidos del servidor. 
        
        Descripcion: Metodo callback que muestra datos de estadisticas si es que estan
                     habilitados.
        
        Retorno: No retorna ningun valor. 
        '''
        
        self.cbModificarEstadisticas(estadisticas)
        
        return
    

    def cargarBotones(self, botones):
        '''
        Metodo: cargarBotones
        
        Parametros: botones: lista de botones habilitados para el usuarios. 
        
        Descripcion: Coordina la habilitacion de las operaciones que puede 
                     realizar el usuario.
        
        Retorno: No retorna ningun valor. 
        '''
        
        self.botones = self.model.Acciones
        self.habilitarBotones()
        self.cbModificarEstado(self.estadoStr)
        
        return
    

    def habilitarBotones(self):
        '''
        Metodo: habilitarBotones
        
        Parametros: No tiene parametros. 
        
        Descripcion: Habilita las botones asociados a las operaciones que 
                     puede realizar el usuario.
        
        Retorno: No retorna ningun valor. 
        '''

        self.botonesActivados = {"ingresar": False,
                                 "apostar": False,
                                 "doblar": False,
                                 "pedir": False,
                                 "plantarse": False,
                                 "stats": False,
                                 "mensaje": False,
                                 "estadisticas": False}
        
        
        for boton in self.botones:
            
            self.botonesActivados[boton] = True
        
        for boton in self.botonesActivados:
            self.habilitarBoton(boton, self.botonesActivados[boton])
            if (boton == 'ingresar' or boton == 'apostar') and self.botonesActivados[boton]:
                self.pIngresar()
        
        return
    

    def habilitarBoton(self, boton, activar):
        '''
        Metodo: habilitarBoton
        
        Parametros: boton: Boton a activar.
                    activar: Boolean que indica si se tiene que activar o no el boton. 
        
        Descripcion: Habilita o deshabilita un boton.
        
        Retorno: No retorna ningun valor. 
        '''
       
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
        elif boton == "doblar":
            self.buttonDoblar.config(state=estado)
        elif boton == "mensaje":
            self.buttonEnviarMensaje.config(state=estado)
        elif boton == "estadisticas":
            self.buttonStats.config(state=estado)
        
        return


    def mostrar(self):
        '''
        Metodo: mostrar
        
        Parametros: No tiene parametros. 
        
        Descripcion: Carga la GUI del juego y la muestra por pantalla.
        
        Retorno: No retorna ningun valor. 
        '''

        self.root.mainloop()
        
        return


    def procesarMonto(self, monto):
    # Cambios def procesarMonto(self, monto):
        '''
        Metodo: procesarMonto
        
        Parametros: No tiene parametros.
        
        Descripcion: Metodo callback llamado al aprietar ENTER sobre el 
                     campo de monto. Si esta activado el boton Ingresar, 
                     se asume que se quiso ingresar dinero, sino se asume 
                     que se quiso apostar.
        
        Retorno: No retorna ningun valor. 
        '''
        
        if self.botonesActivados['ingresar']:
            self.cbIngresar()
        elif self.botonesActivados['apostar']:
            self.cbApostar()
            
        return


    def crearMenu(self):
        '''
        Metodo: crearMenu
        
        Parametros: No tiene parametros.
        
        Descripcion: Crea los botones y campo de ingreso de monto para 
                     que el usuario pueda jugar.
        
        Retorno: No retorna ningun valor. 
        '''
        
        ancho = 12
        colorFront = "white"
        colorBack = "medium blue"
        tamLetra = 12
        tamMonto = 15
 
 
        ''' buttonIngresar: Nivel 1.1.1 - Frame Padre: frameBotones - Posicion: LEFT'''
        self.buttonIngresar = tk.Button(self.frameBotones, width = ancho, height = 20, 
                           text=self.diccionario["ingresar"],
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra, "bold"),
                           command=self.cbIngresar)
        self.buttonIngresar.pack(side=tk.LEFT)

        ''' labelPesos: Nivel 1.1.2 - Frame Padre: frameBotones - Posicion: LEFT'''
        self.labelPesos = tk.Label(self.frameBotones, text="$",width = 1, height = 20,
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra, "bold"))
        self.labelPesos.pack(side=tk.LEFT)

        ''' scrolledMonto: Nivel 1.1.3 - Frame Padre: frameBotones - Posicion: LEFT'''
        self.scrolledMonto = tk.Text(self.frameBotones, width = 10, height = 18, 
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamMonto, "bold"))
        self.scrolledMonto.bind('<Return>', self.procesarMonto)
        self.scrolledMonto.pack(side=tk.LEFT)

        ''' buttonApostar: Nivel 1.1.4 - Frame Padre: frameBotones - Posicion: LEFT'''
        self.buttonApostar = tk.Button(self.frameBotones, width = ancho, height = 20,
                           text=self.diccionario["apostar"],
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra, "bold"),
                           command=self.cbApostar)
        self.buttonApostar.pack(side=tk.LEFT)

        ''' buttonPedir: Nivel 1.1.5 - Frame Padre: frameBotones - Posicion: LEFT'''
        self.buttonPedir = tk.Button(self.frameBotones, width = ancho, height = 20,
                           text=self.diccionario["pedir"],
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra, "bold"),
                           command=self.btPedir)
        self.buttonPedir.pack(side=tk.LEFT)

        ''' buttonPlantarse: Nivel 1.1.6 - Frame Padre: frameBotones - Posicion: LEFT'''
        self.buttonPlantarse = tk.Button(self.frameBotones, width = ancho, height = 20,
                           text=self.diccionario["plantarse"],
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra, "bold"),
                           command=self.cbPlantarse)
        self.buttonPlantarse.pack(side=tk.LEFT)

        ''' buttonDoblar: Nivel 1.1.7 - Frame Padre: frameBotones - Posicion: LEFT'''
        self.buttonDoblar = tk.Button(self.frameBotones, width = ancho, height = 20,
                           text=self.diccionario["doblar"],
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra, "bold"),
                           command=self.cbDoblar)
        self.buttonDoblar.pack(side=tk.LEFT)


        ''' buttonStats: Nivel 1.1.8 - Frame Padre: frameBotones - Posicion: LEFT'''
        self.buttonStats = tk.Button(self.frameBotones, width = ancho, height = 20,
                           text=self.diccionario["stats"],
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra, "bold"),
                           command=self.cbStats)
        self.buttonStats.pack(side=tk.LEFT)

        ''' buttonSalir: Nivel 1.1.9 - Frame Padre: frameBotones - Posicion: LEFT'''
        self.buttonSalir = tk.Button(self.frameBotones, width = ancho, height = 20,
                           text=self.diccionario["salir"],
                           fg=colorFront,
                           bg=colorBack,
                           font=("Arial Bold", tamLetra, "bold"),
                           command=self.cbSalir)
        self.buttonSalir.pack(side=tk.LEFT)
        
        return


    def limpiarTablero(self):
        '''
        Metodo: limpiarTablero
        
        Parametros: No tiene parametros.
        
        Descripcion: Borra todos los objetos creados en el frameCartas para
                     volver a presentar la informacion.
        
        Retorno: No retorna ningun valor. 
        '''
        
        for widget in self.frameCartas.winfo_children():
            widget.destroy()

        return


    def isValidStr(self, cadena, filtro):
        '''
        Metodo: isValidStr
        
        Parametros: cadena: String que se va a validar.
                    filtro: Caracteres que se utilizan como filtro de la cadena
                            para validar que el ingreso un correcto. 
        
        Descripcion: Valida que una cadena string tiene unicamente los caracteres 
                     especificados en filtro. 
        
        Retorno: True: Si cumple con el filtro.
                 False: Si no cumple con el filtro.
        '''
        
        for caracter in cadena:
            if caracter not in filtro:
                return False
            
        return True


    def cbIngresar(self):
        '''
        Metodo: cbIngresar
        
        Parametros: No tiene parametros.
        
        Descripcion: Metodo callback llamado cuando se aprieta el boton de 
                     Ingresar o cuando se aprieta ENTER en el campo monto.
        
        Retorno: No retorna ningun valor. 
        '''
                
        self.cbModificarEstado(self.estadoStr)
        
        monto = self.scrolledMonto.get("1.0", tk.END).replace("\n","")
        if self.isValidStr(monto, list("0123456789".strip())) and len(monto) > 0 and len(monto) <= 10:
            if int(monto) > 0:
                self.model.onFondear(monto)
            
        self.scrolledMonto.delete("0.0", tk.END)
       
        return
    
    
    def btPedir(self):
        '''
        Metodo: cbIngresar
        
        Parametros: No tiene parametros.
        
        Descripcion: Metodo callback llamado cuando se aprieta el boton de 
                     Ingresar o cuando se aprieta ENTER en el campo monto.
        
        Retorno: No retorna ningun valor. 
        '''

        self.model.onPedirCarta()
        return
    
    
    def cbPlantarse(self):
        '''
        Metodo: cbPlantarse
        
        Parametros: No tiene parametros.
        
        Descripcion: Metodo callback llamado cuando se aprieta el boton de 
                     Plantarse.
        
        Retorno: No retorna ningun valor. 
        '''

        self.model.onPlantarse()
        
        return
    
    
    def cbStats(self):
        '''
        Metodo: cbStats
        
        Parametros: No tiene parametros.
        
        Descripcion: Metodo callback llamado cuando se aprieta el boton de 
                     Stats.
        
        Retorno: No retorna ningun valor. 
        '''

        self.model.onSolicitarEstadisticas()
        
        return


    def cbApostar(self):
        '''
        Metodo: cbIngresar
        
        Parametros: No tiene parametros.
        
        Descripcion: Metodo callback llamado cuando se aprieta el boton de 
                     Apostar o cuando se aprieta ENTER en el campo monto.
                             
        Retorno: No retorna ningun valor. 
        '''

        monto = self.scrolledMonto.get("1.0", tk.END).replace("\n","")
        if self.isValidStr(monto, list("0123456789".strip())) and len(monto) > 0 and len(monto) <= 10:
            if int(monto) > 0:
                self.model.onApostar(monto)
            
        self.scrolledMonto.delete("0.0", tk.END)

        
        return
    
    
    def cbDoblar(self):
        '''
        Metodo: cbDoblar
        
        Parametros: No tiene parametros.
        
        Descripcion: Metodo callback llamado cuando se aprieta el boton de 
                     Doblar.
        
        Retorno: No retorna ningun valor. 
        '''

        self.model.onDoblar()
        
        return    

    
    def cbSalir(self):
        '''
        Metodo: cbSalir
        
        Parametros: No tiene parametros.
        
        Descripcion: Metodo callback llamado cuando se aprieta el boton de 
                     Salir. Este cierra el programa.
        
        Retorno: No retorna ningun valor. 
        '''

        self.root.quit()
        os._exit(0)
        
        return    

    
    def enviarMensaje(self):
        '''
        Metodo: enviarMensaje
        
        Parametros: No tiene parametros.
        
        Descripcion: Metodo callback para envar mensajes de usuario. Puede ser 
                     llamado por el boton Enviar o por el metodo procesar mensaje. 
        
        Retorno: No retorna ningun valor. 
        '''

        mensaje = self.entryEnvioMensajes.get("1.0", tk.END)
        self.entryEnvioMensajes.delete("0.0", tk.END)
        self.model.onEnviarMensaje(mensaje)
        
        return


    def crearMenuEnvioMensajes(self):
        '''
        Metodo: crearMenuEnvioMensajes
        
        Parametros: No tiene parametros.
        
        Descripcion: Metodo que crear las pantallas de manejo de mensajes. 
        
        Retorno: No retorna ningun valor. 
        '''

        self.entryEnvioMensajes = ScrolledText(self.frameMenuEntry, font=("Arial Bold", 10))
        self.entryEnvioMensajes.bind('<Return>', self.cbProcesarMensaje)
        self.entryEnvioMensajes.pack()

        self.buttonEnviarMensaje = tk.Button(self.frameMenuButton, width = 48, height = 48,
                           text=self.diccionario["enviar"],
                           fg="white",
                           bg="medium blue",
                           command=self.enviarMensaje)
        self.buttonEnviarMensaje.pack()
        
        return


    def modificarScoreJugador(self, score):
        '''
        Metodo: modificarScoreJugador
        
        Parametros: score: Puntaje obtenido hasta el momento.
        
        Descripcion: Metodo que actualiza el puntaje del usuario. 
        
        Retorno: No retorna ningun valor. 
        '''
        
        self.scoreJugadorStr = score
        self.scoreJugador.set(score)
        
        return
        

    def modificarScoreBanca(self, puntaje, cartas):
        '''
        Metodo: modificarScoreBanca
        
        Parametros: puntaje: Puntaje ontenido hasta el momento.
                    cartas: Cartas de la banca que seran mostradas.
        
        Descripcion: Metodo que actualiza el puntaje de la banca. 
        
        Retorno: No retorna ningun valor. 
        '''

        self.scoreBancaStr = puntaje
        self.scoreBanca.set(puntaje)
        self.cartasBanca = cartas
            
        return

    
    def crearMenuScoreJugador(self, score):
        '''
        Metodo: modificarScoreBanca
        
        Parametros: puntaje: Puntaje ontenido hasta el momento.
                    cartas: Cartas de la banca que seran mostradas.
        
        Descripcion: Metodo que crea las pantalla de informacion de puntaje del usuario. 
        
        Retorno: No retorna ningun valor. 
        '''
        
        self.modificarScoreJugador(score)
        self.labelTituloJugador = tk.Label(self.frameScoreTituloJugador, textvariable=self.nombreJugador, 
                                   font=("Arial Bold", 20, "bold"), bg="medium blue", fg="white")
        self.labelTituloJugador.pack(side=tk.TOP)
        self.labelScoreJugador = tk.Label(self.frameScorePuntajeJugador, textvariable=self.scoreJugador, 
                                   font=("Arial Bold", 80, "bold"), bg="medium blue", fg="white")
        self.labelScoreJugador.pack(side=tk.BOTTOM)

        return

    
    def crearMenuScoreBanca(self, score):
        '''
        Metodo: crearMenuScoreBanca
        
        Parametros: score: Puntaje de la banca obtenido hasta el momento.
                
        Descripcion: Metodo que crea las pantalla de informacion de puntaje de la banca. 
        
        Retorno: No retorna ningun valor. 
        '''
                
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


    def cbJuegoTerminado(self):
        '''
        Metodo: cbJuegoTerminado
        
        Parametros: No tiene parametros.
                
        Descripcion: Metodo callback que es llamado cuando finaliza la mano en curso. 
        
        Retorno: No retorna ningun valor. 
        '''
                        
        scoreBanca = self.scoreBanca
        scoreJugador = self.scoreJugador
        
        # Generar el texto con el estado de la partida 
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
        
        # Se borra las cartas y se muestran las cartas en fortmao reducido
        self.crearCartas(self.cartasBanca, reducir=True, borrar=True, x0=100, y0=0)
        self.crearCartas(self.cartas     , reducir=True,              x0=100, y0=200)
        
        # Se borras y crean los datos del oponente
        for widget in self.frameCartasTitulo.winfo_children():
            widget.destroy()
        self.labelTerminadoBanca = tk.Label(self.frameCartasTitulo, text=estadoBanca, 
                                   font=("Arial Bold", 20, "bold"), bg="green", fg="yellow")
        self.labelTerminadoBanca.pack(side=tk.TOP)
        
        # Se agrega los datos del usuario
        self.labelTerminadoJugador = tk.Label(self.frameCartas, text=estadoJugador, 
                                   font=("Arial Bold", 20, "bold"), bg="green", fg="yellow")
        self.labelTerminadoJugador.pack(side=tk.BOTTOM)

        # Se reproducen audios segun el resultado de la mano        
        if self.estadoStr == "finalizado_perdido":
            self.pPierde()
        elif self.estadoStr == "finalizado_empate":
            self.pEmpata()
        elif self.estadoStr == "finalizado_ganador":
            self.pGana()
        self.comenzado = False
        
        return


    def cbJuegoComenzado(self, mensaje):
        '''
        Metodo: cbJuegoComenzado
        
        Parametros: mensaje: Mensaje recibido del servidr para iniciar la mano.
                
        Descripcion: Metodo callback que es llamado cuando inicia una mano. 
        
        Retorno: No retorna ningun valor. 
        '''

        # Inicializacion
        self.comenzado = True
        self.cartasBancaEnPantalla = False
        self.cbModificarMensajes("SERVIDOR", "\n\n" + "-------------------------\n" + "\n" + mensaje + "\n")
        self.limpiarTablero()
        self.scrolledMonto.focus()
        self.cbModificarEstado("")
        
        return


    def cbModificarEstado(self, estado):
        '''
        Metodo: cbModificarEstado
        
        Parametros: estado: Estado del usuario si es su turno o si esta esperando 
                            alguna accion de otro usuario.
                
        Descripcion: Metodo callback que es llamado cuando cambia el estado del usuario y
                     cando se requiere mostrar cambios en el nombre de usuarioo o saldo. 
        
        Retorno: No retorna ningun valor. 
        '''

        # Inicializacion del estado del usuario: usuario: $ saldo (estado de juego)         
        self.usuario = self.model.MiNombre
        self.estadoStr = estado.replace('[', '').replace(']', '')
        self.estado.set(self.usuario + " " + "$" + str(self.model.MiSaldo) + " (" + self.estadoStr + ")")
        self.modificarScoreJugador(self.model.MiPuntaje)
        cartas = self.model.MisCartas
        
        
        if len(self.cartas) != len(cartas):
            # Si la cantidad de cartas nuevas es diferente que las que habia se regeneran
            for widget in self.frameCartasTitulo.winfo_children():
                widget.destroy()
            self.crearCartas([], borrar=True, comparar=False, x0=20, y0=120)
            self.labelTerminadoBanca = tk.Label(self.frameCartasTitulo, text="BANCA    ", 
                               font=("Arial Bold", 20, "bold"), bg="green", fg="yellow")
            self.labelTerminadoBanca.pack(side=tk.RIGHT)
            self.crearCartas(cartas, borrar=False, comparar=False, x0=20, y0=120)
        else:
            # Si la cantidad de cartas nuevas es igual se vuelven a presentar
            self.crearCartas(cartas, borrar=True, comparar=True, x0=20, y0=120)

        # Si la mano esta en curso y se recibieron las cartas de la banca, se muestran
        if len(self.cartasBanca) > 0 and self.comenzado:
            if self.cartasBanca[0] != "":
                if not self.cartasBancaEnPantalla:
                    self.cartasBancaEnPantalla = True
                    #print(self.cartasBanca)
                    listaCartas = [self.cartasBanca[0], 'reverso']
                    self.crearCartas(listaCartas, reducir=True, borrar=False, x0=450, y0=0)

        self.cartas = cartas
        
        return
        
    
    def crearEstado(self, estado):
        '''
        Metodo: crearEstado
        
        Parametros: estado: Estado del usuario si es su turno o si esta esperando 
                            alguna accion de otro usuario.
                
        Descripcion: Metodo para crear las pantalla de estado del usuario.
        
        Retorno: No retorna ningun valor. 
        '''
        
        self.cbModificarEstado(estado)
        self.labelEstados = tk.Label(self.frameEstadoUsuario, textvariable=self.estado, 
                                   font=("Arial Bold", 25), bg="medium blue", fg="white")
        self.labelEstados.pack(side=tk.LEFT)

        return
    

    def cbModificarEstadisticas(self, estadisticas):
        '''
        Metodo: cbModificarEstadisticas
        
        Parametros: estadisticas: Listado de estadisticas.
                
        Descripcion: Metodo que actualiza la pantalla con las estadisticas del juego.
        
        Retorno: No retorna ningun valor. 
        '''
        
        self.textJugadoresEstadisticas.delete("0.0", tk.END)
        self.textJugadoresEstadisticas.insert(tk.END, estadisticas)
        #self.textJugadoresEstadisticas.see(tk.END)
        self.estadisticasStr = estadisticas
                
        return
    
    
    def cbModificarJugadores(self, jugadores):
        '''
        Metodo: cbModificarJugadores
        
        Parametros: jugadores: Listado del estado de usuarios.
                
        Descripcion: Metodo que actualiza la pantalla de estado de usuarios.
        
        Retorno: No retorna ningun valor. 
        '''
        
        self.textJugadoresInformacion.delete("0.0", tk.END)
        self.textJugadoresInformacion.insert(tk.END, jugadores)
        self.textJugadoresInformacion.see(tk.END)
        self.jugadoresStr = jugadores
                
        return
    
    
    def crearJugadores(self, jugadores):
        '''
        Metodo: crearJugadores
        
        Parametros: jugadores: Listado del estado de usuarios.
                
        Descripcion: Metodo que crear la pantalla de estado de usuarios.
        
        Retorno: No retorna ningun valor. 
        '''

        self.scrollbarJugadoresInformacion = tk.Scrollbar(self.frameJugadoresInformacion) 
        self.textJugadoresInformacion = tk.Text(self.frameJugadoresInformacion, width = 622, height = 74,
                                font=("Arial Bold", 15), fg="black", bg="white")
        self.scrollbarJugadoresInformacion.pack(side=tk.RIGHT, fill=tk.Y)
        self.textJugadoresInformacion.pack(side=tk.LEFT, fill=tk.Y)
        self.scrollbarJugadoresInformacion.config(command=self.textJugadoresInformacion.yview)
        self.textJugadoresInformacion.config(yscrollcommand=self.scrollbarJugadoresInformacion.set)

        self.cbModificarJugadores(jugadores)
        self.textJugadoresInformacion.pack(side=tk.LEFT)

        self.scrollbarJugadoresEstadisticas = tk.Scrollbar(self.frameJugadoresEstadisticas) 
        self.textJugadoresEstadisticas = tk.Text(self.frameJugadoresEstadisticas, width = 622, height = 74,
                                font=("Arial Bold", 15), fg="black", bg="white")
        self.scrollbarJugadoresEstadisticas.pack(side=tk.RIGHT, fill=tk.Y)
        self.textJugadoresEstadisticas.pack(side=tk.LEFT, fill=tk.Y)
        self.scrollbarJugadoresEstadisticas.config(command=self.textJugadoresEstadisticas.yview)
        self.textJugadoresEstadisticas.config(yscrollcommand=self.scrollbarJugadoresEstadisticas.set)

        #self.cbModificarJugadores(jugadores)
        self.textJugadoresEstadisticas.pack(side=tk.LEFT)

        
        return


    def cbProcesarMensaje(self):
        '''
        Metodo: cbProcesarMensaje
        
        Parametros: No tiene parametros.
                
        Descripcion: Metodo callback que es llamado cuando se aprieta ENTER desde el 
                     menu de envio de mensajes.
        
        Retorno: No retorna ningun valor. 
        '''
        
        if self.botonesActivados['mensaje']:
            self.enviarMensaje()
            
        return

    
    def cbModificarMensajes(self, mensajes, tipo):
        '''
        Metodo: cbModificarMensajes
        
        Parametros: mensajes: Mensaje recibido.
                    tipo: Tipo de mensaje recibido.
                
        Descripcion: Metodo callback que es llamado cuando se recibe 
                     un neuvo mensaje.
        
        Retorno: No retorna ningun valor. 
        '''
        
        if tipo == "SERVIDOR":
            self.textChatServidor.insert(tk.END, mensajes + "\n")
            self.textChatServidor.see(tk.END)
        elif tipo == "MENSAJE":
            self.textChatMensajes.insert(tk.END, mensajes + "\n")
            self.textChatMensajes.see(tk.END)
        
        return
        
    
    def crearMenuMensajes(self, mensajes):
        '''
        Metodo: crearMenuMensajes
        
        Parametros: mensajes: Mensaje recibido.
                
        Descripcion: Crea la pantalla del menu de mensajes.
        
        Retorno: No retorna ningun valor. 
        '''

        # Creacion del menu de mensajes de Servidor.
        self.scrollbarChatServidor = tk.Scrollbar(self.frameChatPanelServidor) 
        self.textChatServidor = tk.Text(self.frameChatPanelServidor, width=388, height=200,
                                font=("Arial Bold", 12), fg="blue", bg="white")
        self.scrollbarChatServidor.pack(side=tk.RIGHT, fill=tk.Y)
        self.textChatServidor.pack(side=tk.LEFT, fill=tk.Y)
        self.scrollbarChatServidor.config(command=self.textChatServidor.yview)
        self.textChatServidor.config(yscrollcommand=self.scrollbarChatServidor.set)
        self.textChatServidor.pack(side=tk.LEFT)

        # Creacion del menu de mensajes de usuarios.
        self.scrollbarChatMensajes = tk.Scrollbar(self.frameChatPanelMensajes) 
        self.textChatMensajes = tk.Text(self.frameChatPanelMensajes, width=388, height=200,
                                font=("Arial Bold", 12), fg="blue", bg="white")
        self.scrollbarChatMensajes.pack(side=tk.RIGHT, fill=tk.Y)
        self.textChatMensajes.pack(side=tk.LEFT, fill=tk.Y)
        self.scrollbarChatMensajes.config(command=self.textChatMensajes.yview)
        self.textChatMensajes.config(yscrollcommand=self.scrollbarChatMensajes.set)
        self.textChatMensajes.pack(side=tk.LEFT)

        return

    
    def crearCartas(self, cartas, reducir=False, borrar=False, invertir=False, comparar=False, x0=0, y0=0):
        '''
        Metodo: crearMenuMensajes
        
        Parametros: cartas: Lista de cartas a crear.
                    reducir: Boolean que indica si hay que achicar las cartas o no.
                    borrar: Boolean que indica si hay que borrar las cartas o no.
                    invertir: Boolean que indica si hay que invertir la forma de crear
                              las cartas o no.
                    comparar: Boolean que indica si hay que comparar las cartas 
                              nuevas con las existenes o no.
                    x0: Posicion inicial horizaontal (x) de la primera carta.
                    y0: Posicion incial vertical (y) de la primera carta.
                
        Descripcion: Crea las cartas indicadas en la lista.
        
        Retorno: No retorna ningun valor. 
        '''


        if len(cartas) == 0:
            #print('no hay cartas')
            return

        if len(cartas) == len(self.cartas) and comparar:
            iguales = True
            for i in range(0, len(cartas)):
                if cartas[i] != self.cartas[i]:
                    #print('cartas diferentes')
                    iguales = False
                    break
            
            if iguales == True:
                #print('Ya se estan mostrando esas cartas')
                return
            
        #print('Tengo cartas')
        #print(cartas)
        #self.cartas = cartas
        
        # Si no existe se crea la pantalla de cartas.
        if self.app == None:
            self.app = PantallaImagenes(self.frameCartas)
            self.app['bg']='green'
        else:
            if borrar:
                self.app.borrar()
        
        # Se inicializan los parametros.
        self.cwd = os.getcwd()
        mazo = 'mazo'
        self.imgList = []
        xOffset = 60
        yOffset = 5
        yLineOffset = 60
        factorInversion = 1
        
        # Se verifica si hay que invertir las cartas.
        if invertir:
            factorInversion = -1

        cartasPorLinea = 7
        # Se acomodan las cartas
        if len(cartas) <= cartasPorLinea and 'reverso' not in cartas:
            x0 = x0 + int(xOffset/2) * (7-len(cartas))
        
        x = x0
        y = y0
        if len(cartas) <= cartasPorLinea and y0 >= 100:
            # se mejor la visivilidad de las cartas segun esten en el margen inferior 
            y = y + yOffset*cartasPorLinea
            
        for i in range(0, len(cartas)):
            
            self.imgList.append(os.path.join(os.path.join(self.cwd, mazo), cartas[i] + '.jpg'))
            #self.imgList.append(os.path.join(os.path.join(self.cwd, mazo), self.cartas[i] + '.jpg'))
            #print(x,y)
            if reducir:
                self.app.agregar(self.imgList[i], x=x, y=y, width = 90, height = 126)
                #self.app.agregar(self.imgList[i], x=x, y=y, width = 135, height = 189)
            else:
                self.app.agregar(self.imgList[i], x=x, y=y, width = 158, height = 221)

            x = x + xOffset * factorInversion 
            y = y + yOffset 
            if (i+1) % cartasPorLinea == 0:
                x = x0
                if not reducir:
                    y = y0 + int((i/cartasPorLinea)*yLineOffset)
                    #print(y)
 
        return


def testPantallaPedirCarta():
    '''
    Metodo: testPantallaPedirCarta
    
    Parametros: No tiene parametros. 
            
    Descripcion: Metodo para pruebas de interface GUI.
    
    Retorno: No retorna ningun valor. 
    '''
    
    print("hola carta")
    
    return


def testPantallaInicializador():
    '''
    Metodo: testPantallaInicializador
    
    Parametros: No tiene parametros. 
            
    Descripcion: Metodo para pruebas de interface GUI.
    
    Retorno: No retorna ningun valor. 
    '''

    cartas1 = ['1-3', '2-4', '3-5']
    cartas2 = ['1-3', '2-4', '3-5', '1-3', '2-4', '3-5']
    cartas = ['1-3', '2-4', '3-5', '4-2', '1-4', '2-2', '1-3', '2-4', '3-5', '4-2', '1-4', '2-2', '1-3', '2-4']
    listaCartas = []
    model = GuiViewModel()
    model.MiSaldo = 3000
    model.MisCartas = cartas1
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
    bjScreen.cbModificarEstado("Jugar")
    bjScreen.botones = ['apostar', 'stats']
    bjScreen.cbJuegoTerminado()
    #668-90-20, 20
    #20, 320
    bjScreen.mostrar()

    '''    
    bjScreen.crearCartas(listaCartas)
    bjScreen.crearMenuScoreJugador("12")
    bjScreen.crearEstado("Jugar")
    bjScreen.crearJugadores("Quique: Esperando\nSeba: Esperando\nFede G: Esperando\nFede F: Jugando\nRichard: Esperando")
    bjScreen.crearMenuMensajes("Quique: Esperando...\n")
    bjScreen.mostrar()
    
    test=input("prueba")
    '''


if __name__ == "__main__":

    testPantallaInicializador()
    
    