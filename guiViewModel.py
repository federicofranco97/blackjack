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



class GuiViewModel(Observer):
    def __init__(self):
        self.MiNombre = "sebastian"
        self.MiPuntaje = 100
        self.MisCartas = []
        self.Turno = "sebastian"
        self.Acciones = []

        Observer.__init__(self)

    def onPedirCarta(self):
        Event('pedirCartaEvent')

    def onRefreshButtons(self, botones):
        self.Acciones = botones
        Event('refreshButtonsEvent')






