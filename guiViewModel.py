from pymitter import EventEmitter

class GuiViewModel():
    def __init__(self):
        self.ee = EventEmitter()
        self.MiNombre = "..."
        self.MiPuntaje = 0
        self.MisCartas = []
        self.MiSaldo = 0
        self.MiEstado = ""

        self.esMiTurno = False
        self.Turno = ""
        self.Acciones = []
        self.Jugadores = []

    def onRequestConnection(self, servidor, puerto):
        return self.ee.emit("requestConnectionEvent", servidor, puerto)

    def onSoy(self, soy):
        self.ee.emit("soyEvent", soy)

    def onSoyAceptado(self):
        self.ee.emit("soyAceptadoEvent", )

    def onSoyRechazado(self):
        self.ee.emit("soyRechazadoEvent", )

    def onConnected(self):
        self.ee.emit("connectedEvent", )

    def onConnectError(self, mensaje):
        self.ee.emit("connectErrorEvent", mensaje)

    def onEntered(self):
        self.ee.emit("enteredEvent", )

    def onPedirCarta(self):
        self.ee.emit("pedirCartaEvent", )

    def onPlantarse(self):
        self.ee.emit("plantarseEvent", )

    def onSeparar(self):
        self.ee.emit("separarEvent", )

    def onDoblar(self):
        self.ee.emit("doblarEvent", )

    def onFondear(self, monto):
        self.ee.emit("fondearEvent", monto)

    def onApostar(self, monto):
        self.ee.emit("apostarEvent", monto)

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








