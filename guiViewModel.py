from pymitter import EventEmitter

#Clase que hace de interfaz entre la GUI y el Cliente
class GuiViewModel():
    def __init__(self):
        self.ee = EventEmitter()
        self.MiNombre = "..."
        self.MiPuntaje = 0
        self.MisCartas = []
        self.MiSaldo = 0
        self.MiEstado = ""
        self.Validado = False

        self.esMiTurno = False
        self.Turno = ""
        self.Acciones = []
        self.Jugadores = []
        self.lenguaje = "es"

    #Evento que lanza la GUI para pedir conexion a traves del cliente
    def onRequestConnection(self, servidor, puerto):
        return self.ee.emit("requestConnectionEvent", servidor, puerto)

    #Evento que envia la GUI para enviar un comando SOY
    def onSoy(self, soy):
        self.ee.emit("soyEvent", soy)

    #Evento que envia el Cliente a la GUI para avisarle que fue aceptado en la Sala
    def onSoyAceptado(self):
        self.ee.emit("soyAceptadoEvent", )

    #Evento que envia el Cliente a la GUI para avisarle que se rechazo el ingreso a la Sala
    def onSoyRechazado(self, mensaje):
        self.ee.emit("soyRechazadoEvent", mensaje)

    #Evento que indica a la GUI que la conexion se establecio correctamente
    def onConnected(self):
        self.ee.emit("connectedEvent", )

    #Evento que le indica a la GUI que fallo la conexion
    def onConnectError(self, mensaje):
        self.ee.emit("connectErrorEvent", mensaje)

    #Evento que dispara la GUI para solicitar una carta
    def onPedirCarta(self):
        self.ee.emit("pedirCartaEvent", )

    #Evento que dispara la GUI para plantarse
    def onPlantarse(self):
        self.ee.emit("plantarseEvent", )

    #Evento que dispara la GUI para duplicar la apuesta
    def onDoblar(self):
        self.ee.emit("doblarEvent", )

    #Evento que dispara la GUI para ingresar dinero
    def onFondear(self, monto):
        self.ee.emit("fondearEvent", monto)

    #Evento que dispara la GUI para ingresar una apuesta
    def onApostar(self, monto):
        self.ee.emit("apostarEvent", monto)

    #Evento que dispara la GUI para enviar un mensaje de chat
    def onEnviarMensaje(self, mensaje):
        self.ee.emit("enviarMensajeEvent", mensaje)

    #Evento que informa a la GUI de los botones que tiene habilitados en cada momento
    def onRefreshButtons(self, botones):
        self.Acciones = botones
        self.ee.emit("refreshButtonsEvent", (botones))

    #Evento que indica a la GUI cuando cambia el turno de la partida
    def onTurnoChanged(self, turno):
        self.Turno = turno
        self.esMiTurno = self.MiNombre == turno
        self.ee.emit("turnoChangedEvent", turno)

    #Evento que indica a la GUI cuando llega un mensaje entrante
    def onMensajeEntrante(self, mensaje, tipo):
        self.ee.emit("mensajeEntranteEvent", mensaje, tipo)

    #Evento que indica cuando comienza una partida nueva
    def onJuegoComenzado(self, mensaje):
        self.ee.emit("juegoComenzadoEvent", mensaje)

    #Evento que indica que la partida termino
    def onJuegoTerminado(self):
        self.ee.emit("juegoTerminadoEvent", )

    #Evento que notifica que algun dato cambio, estado, puntaje, etc.
    def onEstadoChanged(self, estado):
        self.ee.emit("estadoChangedEvent", estado)

    #Evento que indica que el status de los otros jugadores cambio
    def onJugadoresRefreshed(self, status):
        self.ee.emit("jugadoresRefreshedEvent", status)

    #Evento que reporta el cambio de estado de la mano de la banca
    def onPuntajeBancaChanged(self, puntaje, cartas):
        self.ee.emit("puntajeBancaChangedEvent", puntaje, cartas)

    def onSolicitarEstadisticas(self):
        self.ee.emit("solicitarEstadisticasEvent", )

    def onEstadisticasRecibidas(self, estadisticas):
        self.ee.emit("estadisticasRecibidasEvent", estadisticas)








