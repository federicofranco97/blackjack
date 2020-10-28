from threading import Timer

"""
    Subclase de excepcion, para los nombres usados
"""
class NombreUsado(Exception):
    pass

"""
    Clase que representa a un jugador de blackjack
"""
class Jugador():

    def __init__(self, instanciaUsuario):
        self.usuario = instanciaUsuario
        self.dinero = 0

    def enviarMensaje(self, mensaje):
        self.usuario.enviarMensaje("[Servidor] " + mensaje)

"""
    Clase que representa a una carta
"""
class Carta():

    def __init__(self, valor, palo):
        self.valor = valor
        self.palo = palo

"""
    Coordinador del juego
"""
class Blackjack():

    def __init__(self):
        self.jugadores = {}
        self.jugadoresActivos = {}
        self.jugadoresEsperando = {}
        self.rondaActiva = False
        self.interrumpirTimer = False
        self.segundosTotales = 0

    def empezarTimer(self):
        segundosRestantes = 30-self.segundosTotales
        self.notificarJugadores("Empieza el juego en " + str(segundosRestantes) + "segundos")
        self.segundosTotales += 1
        if segundosRestantes > 0:
            Timer(1.0, self.empezarTimer).start()

    def _notificarJugadores(self, jugadores, mensaje):
        for jug in jugadores:
            jugadores[jug].enviarMensaje(mensaje)

    def notificarJugadores(self, mensaje):
        self._notificarJugadores(self.jugadores, mensaje)

    def notificarJugadoresActivos(self, mensaje):
        self._notificarJugadores(self.jugadoresActivos, mensaje)

    def agregarJugador(self, usuario):
        if usuario.nombre in self.jugadores:
            usuario.enviarMensaje("Ya existe un usuario con ese nombre")
        self.interrumpirTimer = True
        nuevoJugador = Jugador(usuario)
        nuevoJugador.enviarMensaje("Bienvenido " + usuario.nombre + "")
        self.jugadores[usuario.nombre] = nuevoJugador
        self.notificarJugadores(usuario.nombre + " se unio al juego")

    
    def obtenerEstadisticas(self):
        cantJugadores = "Cantidad jugadores: " + str(len(self.jugadores))
        return cantJugadores

    def ingresarDinero(self, usuario, monto):
        jugador = self.jugadores[usuario]
        if int(monto) <= 0:
            jugador.enviarMensaje("Debes ingresar un saldo positivo")
        if self.rondaActiva == False and jugador != None:
            jugador.dinero += int(monto)
            jugador.enviarMensaje("Tu nuevo saldo es de " + str(jugador.dinero))

    def iniciarPartida(self, usuario):
        jugador = self.jugadores[usuario]
        if self.rondaActiva == True:
            if self.jugadoresActivos[usuario] != None:
                jugador.enviarMensaje("Hay una ronda en curso, no te podes unir")
            else:
                jugador.enviarMensaje("Ya estás jugando en la ronda, y la partida ya esta iniciada")
        else:
            self.empezarTimer()
            




            


