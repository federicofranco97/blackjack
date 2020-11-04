"""
class Observer:
    _observers = []

    def __init__(self):
        self._observers.append(self)
        self._observed_events = []

    def observe(self, event_name, callback_fn):
        self._observed_events.append({'event_name': event_name, 'callback_fn': callback_fn})


class Event:
    def __init__(self, event_name, *callback_args):
        for observer in Observer._observers:
            for observable in observer._observed_events:
                if observable['event_name'] == event_name:
                    observable['callback_fn'](*callback_args)

"""
from pymitter import EventEmitter


class GuiViewModel():
    def __init__(self):
        self.ee = EventEmitter()
        self.MiNombre = "sebastian"
        self.MiPuntaje = 100
        self.MisCartas = []
        self.Turno = "sebastian"
        self.Acciones = []
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


    def onRefreshButtons(self, botones):
        self.Acciones = botones
        self.ee.emit("refreshButtonsEvent", (botones))

    def onTurnoChanged(self, turno):
        self.miTurno = self.MiNombre == turno
        self.ee.emit("turnoChangedEvent", (turno))

    def onMensajeEntrante(self, mensaje):
        self.ee.emit("mensajeEntranteEvent", (mensaje))

    def onJuegoComenzado(self):
        self.ee.emit("juegoComenzadoEvent", )









