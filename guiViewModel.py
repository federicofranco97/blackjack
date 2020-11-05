from pymitter import EventEmitter

class GuiViewModel():
    def __init__(self):
        self.ee = EventEmitter()
        self.MiNombre = "sebastian"
        self.MiPuntaje = 100
        self.MisCartas = []
        self.MiSaldo = 100
        self.MiEstado = ""


        self.esMiTurno = False
        self.Turno = "sebastian"
        self.Acciones = []
        self.Jugadores = []
        #Observer.__init__(self)

    def onPedirCarta(self):
        self.ee.emit("pedirCartaEvent", )

    def onPlantarse(self):
        self.ee.emit("plantarseEvent", )

    def onSeparar(self):
        self.ee.emit("separarEvent", )

    def onDoblar(self):
        self.ee.emit("doblarEvent", )

    def onFondear(self, monto):
        self.ee.emit("fondearEvent", )

    def onApostar(self, monto):
        self.ee.emit("apostarEvent", )

    def onEnviarMensaje(self, mensaje):
        self.ee.emit("enviarMensajeEvent", (mensaje))

    def onRefreshButtons(self, botones):
        self.Acciones = botones
        self.ee.emit("refreshButtonsEvent", (botones))

    def onTurnoChanged(self, turno):
        self.Turno = turno
        self.esMiTurno = self.MiNombre == turno
        self.ee.emit("turnoChangedEvent", (turno))

    def onMensajeEntrante(self, mensaje):
        self.ee.emit("mensajeEntranteEvent", (mensaje))

    def onJuegoComenzado(self):
        self.ee.emit("juegoComenzadoEvent", )

    def onJuegoTerminado(self, ganador):
        self.ee.emit("juegoTerminadoEvent", )

    def onEstadoChanged(self, estado):
        self.ee.emit("estadoChangedEvent", estado)

    def onJugadoresRefreshed(self, status):
        self.ee.emit("jugadoresRefreshedEvent", status)

    def onPuntajeBancaChanged(self, puntaje):
        self.ee.emit("puntajeBancaChangedEvent", puntaje)








