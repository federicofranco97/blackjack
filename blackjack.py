from threading import Timer
import random
"""
    Subclase de excepcion, para cuando hay un nombre duplicado
"""
class NombreUsado(Exception):
    pass

"""
    Clase que representa a un jugador de blackjack
"""
class Jugador():

    def __init__(self, instanciaUsuario):
        self.usuario = instanciaUsuario
        self.manos = []
        self.manoActual = None

    def enviarMensaje(self, mensaje):
        self.usuario.enviarMensaje("[Servidor] " + mensaje)

    def agregarMano(self, mano):
        self.manos.append(mano)

    def iniciarTurno(self):
        self.manos = []
        nuevaMano = Mano()
        self.agregarMano(nuevaMano)
        self.manoActual = nuevaMano
        self.enviarMensaje("Es tu turno")

    def doblarApuesta(self, monto):
        self.manoActual.apuesta *= 2

    def apostar(self, monto):
        if self.manoActual.estado == "sin_apuesta":
            self.manoActual.apuesta = monto
            self.manoActual.estado = "iniciada"
        else:
            self.enviarMensaje("Ya hiciste la apuesta")

    def totalApostado(self):
        total = 0
        for mano in self.manos:
            total += mano.apuesta
        return total

    def pedir(self, carta):
        if self.manoActual.estado == "iniciada":
            self.manoActual.agregarCarta(carta)
            puntajeMano = self.manoActual.obtenerPuntaje()
            self.enviarMensaje("El total de tu mano es " + str(puntajeMano))
            return puntajeMano
        else:
            self.enviarMensaje("No puedes pedir una carta en este momento")

    def finalizarMano(self):
        self.manoActual.estado = "finalizada_ido"

    def plantarse(self):
        if self.manoActual.estado == "iniciada":
            self.manoActual.estado = "esperando_banca"
        else:
            self.enviarMensaje("No puedes plantarse, esta mano ya esta terminada")




"""
    Clase que representa una mano
"""
class Mano():

    def __init__(self):
        self.apuesta = 0
        self.estado = "sin_apuesta"
        self.cartas = []

    def agregarApuesta(self, monto):
        self.apuesta += monto

    def agregarCarta(self, carta):
        self.cartas.append(carta)

    def obtenerPuntaje(self):
        total = 0
        for carta in self.cartas:
            valor = carta.valor
            if valor == 11 or valor == 12 or valor == 13:
                total += 10
            elif valor == 14:
                if total >= 11: total += 1
                if total < 11: total += 11
            else:
                total += valor
        return total


"""
    Clase que representa a una carta
"""
class Carta():

    def __init__(self, valor, palo):
        self.valor = valor
        self.palo = palo

class Mazo():

    def __init__(self):
        self.cartas = []

    def shuffle(self):
        mix = []
        for z in range(4):
            for x in range(13):
                for y in range(4):
                    mix.append(Carta(x, y))
        print(len(mix))
        random.shuffle(mix)
        self.cartas = mix.copy()

    def proximaCarta(self):
        return self.cartas.pop()


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
        self.jugadorActual = None
        self.iterador = None
        self.timerIniciado = False
        self.segundosTotales = 0
        self.mazo = None

    def empezarTimer(self):
        self.timerIniciado = True
        segundosRestantes = 60-self.segundosTotales
        self.notificarJugadores("Empieza el juego en " + str(segundosRestantes) + "segundos")
        self.segundosTotales += 1
        if segundosRestantes > 0:
            Timer(1.0, self.empezarTimer).start()
        else:
            self.timerIniciado = False
            self.rondaActiva = True
            self.mazo = Mazo()
            self.mazo.shuffle()
            self.jugadoresActivos = self.jugadores.copy()
            self.iterador = iter(self.jugadoresActivos)
            self.jugadorActual = self.jugadoresActivos[next(self.iterador)]
            self.jugadorActual.iniciarTurno()
            

    def _notificarJugadores(self, jugadores, mensaje):
        for jug in jugadores:
            jugadores[jug].enviarMensaje(mensaje)

    def notificarJugadores(self, mensaje):
        self._notificarJugadores(self.jugadores, mensaje)

    def notificarJugadoresActivos(self, mensaje):
        self._notificarJugadores(self.jugadoresActivos, mensaje)

    def decidirUsuario(self, jugador):
        if self.rondaActiva == True:
            self.jugadoresEsperando[jugador.usuario.nombre] = jugador
            jugador.enviarMensaje("Hay una ronda activa, una vez finalizada se te unirá automaticamnete. Puedes irte de la espera con el comando retirarse")
        else:
            if self.timerIniciado == False:
                jugador.enviarMensaje("Iniciando cuenta regresiva para iniciar el juego")
                self.empezarTimer()
            else:
                jugador.enviarMensaje("Una vez finalizada la cuenta regresiva")


    def agregarJugador(self, usuario):
        if usuario.nombre in self.jugadores:
            usuario.enviarMensaje("Ya existe un usuario con ese nombre")
        self.interrumpirTimer = True
        nuevoJugador = Jugador(usuario)
        nuevoJugador.enviarMensaje("Bienvenido " + usuario.nombre + "")
        self.jugadores[usuario.nombre] = nuevoJugador
        self.notificarJugadores(usuario.nombre + " se unio al juego")
        self.decidirUsuario(nuevoJugador)
    
    def obtenerEstadisticas(self):
        cantJugadores = "Cantidad jugadores: " + str(len(self.jugadores))
        return cantJugadores

    def apostar(self, usuario, monto):
        if not self.jugadorActual.usuario.nombre  == usuario:
            usuario.enviarMensaje("No es tu turno")
        else:
            self.jugadorActual.apostar(monto)

    def rotarJugador(self):
        self.jugadorActual = self.jugadoresActivos[next(self.iterador)]
        self.jugadorActual.iniciarTurno()

    def pedir(self, usuario):
        if not self.jugadorActual.usuario.nombre  == usuario:
            usuario.enviarMensaje("No es tu turno")
        else:
            proxima = self.mazo.proximaCarta()
            puntajeTotal = self.jugadorActual.pedir(proxima)
            if puntajeTotal > 21:
                self.jugadorActual.finalizarMano()
                self.rotarJugador()



    def plantarse(self, usuario):
        if not self.jugadorActual.usuario.nombre  == usuario:
            usuario.enviarMensaje("No es tu turno")
        else:
            self.jugadorActual.plantarse()
            self.rotarJugador()

    def doblar(self, usuario):
        if not self.jugadorActual.usuario.nombre  == usuario:
            usuario.enviarMensaje("No es tu turno")
        else:
            self.jugadorActual.manoActual.doblarApuesta()
            proxima = self.mazo.proximaCarta()
            puntajeTotal = self.jugadorActual.pedir(proxima)
            if puntajeTotal > 21:
                self.jugadorActual.finalizarMano()
                self.jugadorActual.enviarMensaje("Perdiste con un puntaje de " + str(puntajeTotal))
            self.rotarJugador()            

        





            


