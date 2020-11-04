from threading import Timer
from mazo import Mazo, Carta, Mano
from excepciones import NombreUsado, DineroInsuficiente, ApuestaRealizada, JugadorInexistente, ComandoNoPermitido
from jugador import Jugador, Banca
import copy

"""
    Coordinador del juego. Se encarga de todo aquello que excede los limites del jugador en si mismo. Coordina las rondas y mantiene
    el estado general del kjuego.
"""

class Blackjack():

    def __init__(self):
        self.estadoActual = None
        self.jugadores = {}
        self.jugadoresActivos = {}
        self.jugadoresActivosSet = {}
        self.jugadorActualIndice = None
        self.jugadoresEsperando = {}
        self.rondaActiva = False
        self.interrumpirTimer = False
        self.jugadorActual = None
        self.timerIniciado = False
        self.banca = Banca()
        self.segundosTotales = 0
        self.mazo = None

    """
        Esta funcion se llama desde el thread que esta escuchando el socket de los usuarios cuando no puede enviar un mensaje porque el socket
        esta cerrado. Esto dispara remover al jugador del juego.
    """
    def removerJugador(self, usuario):
        if self.jugadores.has_key(usuario) == False:
            return
        del self.jugadores[usuario]
        del self.jugadoresActivosSet[usuario]
        for i in range(len(self.jugadoresActivos)):
            if self.jugadoresActivos[i] == usuario:
                del self.jugadoresActivos[i]
        if not self.jugadorActual == None:
            if self.jugadorActual.usuario.nombre == usuario:
                self.jugadorActualIndice = self.jugadorActualIndice-1
                self.rotarJugador()
        self.notificarJugadores("el usuario " + usuario + " abandono la sala")


    """
        Esta funcion se utiliza para enviar un mensaje a una lista de jugadores. Es una funcion pseudo-privada, no deberia ser llamada directamente, sino
        a traves de notificarJugadores o notificarJugadoresActivos.
    """
    def _notificarJugadores(self, jugadores, mensaje):
        for jug in jugadores:
            jugadores[jug].enviarMensaje(mensaje)

    """
        Esta funcion envia un mensaje a todos los jugadores, activos o no.
    """
    def notificarJugadores(self, mensaje):
        self._notificarJugadores(self.jugadores, mensaje)

    """
        Esta funcion envia un mensaje a los jugadores que estan participando de la ronda.
    """
    def notificarJugadoresActivos(self, mensaje):
        self._notificarJugadores(self.jugadoresActivosSet, mensaje)

    """
        Obtiene la referencia de un jugador para utilizarlo.
    """
    def _obtenerJugador(self, nombre):
        jugador = self.jugadores[nombre]
        if jugador == None:
            raise JugadorInexistente()
        return jugador

    """
        Devuelve verdadero si el jugador actual tiene el nombre del argumento.
    """
    def _esJugadorActual(self, nombre):
        if self.jugadorActual == None:
            return False
        return self.jugadorActual.usuario.nombre == nombre

    """
        Empieza la cuenta regresiva para iniciar el juego, y resetea el estado general del mismo.
    """
    def empezarTimer(self):
        self.timerIniciado = True
        segundosRestantes = 60-self.segundosTotales
        if segundosRestantes % 10 == 0:
            self.notificarJugadores("empieza el juego en " + str(segundosRestantes) + " segundos")
        self.segundosTotales += 1
        if segundosRestantes > 0:
            Timer(1.0, self.empezarTimer).start()
        else:
            self.timerIniciado = False
            self.rondaActiva = True
            self.mazo = Mazo()
            self.mazo.mezclar()
            self.jugadoresActivosSet = self.jugadores.copy()
            self.jugadoresActivos = list(self.jugadoresActivosSet)
            self.estadoActual = "pendiente_apuestas"
            self.banca.iniciarTurno()
            for i in self.jugadoresActivos:
                self.jugadoresActivosSet[i].esperandoApuesta()

    """
        Cuando se conecta un usuario nuevo, esta funcion decide si colocarlo en la lista de espera o no.
    """
    def decidirUsuario(self, jugador):
        if self.rondaActiva == True:
            self.jugadoresEsperando[jugador.usuario.nombre] = jugador
            jugador.enviarMensaje("hay una ronda activa, una vez finalizada se te unirá automaticamente. Puedes irte de la espera cerrando la conexion.")
        else:
            if self.timerIniciado == False:
                jugador.enviarMensaje("iniciaremos cuenta regresiva para iniciar el juego")
                self.empezarTimer()
            else:
                jugador.enviarMensaje("una vez finalizada la cuenta regresiva")

    """
        Esta funcion maneja la peticion de agregar un jugador al juego.
    """
    def agregarJugador(self, usuario):
        if usuario.nombre in self.jugadores:
            usuario.enviarMensaje("Ya existe un usuario con ese nombre")
        else:
            self.interrumpirTimer = True
            nuevoJugador = Jugador(usuario)
            nuevoJugador.enviarMensaje("Bienvenido " + usuario.nombre + "")
            self.jugadores[usuario.nombre] = nuevoJugador
            self.notificarJugadores(usuario.nombre + " se unio al juego")
            self.decidirUsuario(nuevoJugador)
    
    """
        Devuelve la cantidad de jugadores
    """
    def obtenerEstadisticas(self):
        cantJugadores = "Cantidad jugadores: " + str(len(self.jugadores))
        return cantJugadores

    """
        Funciona que chequea si el juego debe comenzar, es decir, si el resto de los participanes ya hizo una apuesta.
        De haber hecho todas las apuestas, se reparten las primeras cartas.
    """
    def _deberiaEmpezar(self):
        apuestasPendientes = 0
        for i in self.jugadoresActivos:
            if self.jugadoresActivosSet[i].apuestaInicial == None:
                apuestasPendientes += 1
        if apuestasPendientes == 0:
            for ronda in range(2):
                for indiceAct in range(len(self.jugadoresActivos)):
                    nombreJugador = self.jugadoresActivos[indiceAct]
                    jugadorActual = self.jugadoresActivosSet[nombreJugador]
                    proximaCarta = self.mazo.proximaCarta()
                    jugadorActual.pedir(proximaCarta)
                cartaBanca = self.mazo.proximaCarta()
                if ronda == 1:
                    cartaBanca.visible = False
                self.banca.mano.agregarCarta(cartaBanca)
            self.notificarJugadoresActivos("La banca tiene " + self.banca.mano.obtenerDescripcionCompleta())
            self.jugadorActualIndice = 0
            self.jugadorActual = self.jugadoresActivosSet[self.jugadoresActivos[0]]
            self.notificarJugadoresActivos("es el turno de " + self.jugadorActual.usuario.nombre)


    """
        Esta funcion maneja la peticion de apuesta de los usuarios.
    """
    def apostar(self, usuario, monto):
        _jugador = self._obtenerJugador(usuario)
        try:
            _jugador.apostar(monto)
            self._deberiaEmpezar()
        except DineroInsuficiente:
            _jugador.enviarMensaje("No tienes el dinero suficiente")
        except ApuestaRealizada:
            _jugador.enviarMensaje("Ya realizaste la apuesta de esta mano")

    """
        Funcion que rota los jugadores y, en caso que ya no queden mas para rotar, hace jugar a la banca.
    """
    def rotarJugador(self):
        if len(self.jugadoresActivos) == (self.jugadorActualIndice+1):
            self.notificarJugadoresActivos("ahora jugara la banca")
            self.banca.mano.mostrarTodas()
            self.notificarJugadoresActivos("la banca mostrar su carta oculta")
            self.notificarJugadoresActivos("la banca tiene: " + self.banca.mano.obtenerDescripcionCompleta())
            while self.banca.mano.obtenerPuntaje() <= 16:
                proxCarta = self.mazo.proximaCarta()
                self.banca.mano.agregarCarta(proxCarta)
                self.notificarJugadoresActivos("la banca tiene: " + self.banca.mano.obtenerDescripcionCompleta())
            puntaje = self.banca.mano.obtenerPuntaje()
            for jugador in self.jugadoresActivos:
                _jug = self.jugadoresActivosSet[jugador]
                if _jug.estadoActual == "finalizado_pendiente" and (_jug.manoActual.obtenerPuntaje() > puntaje or puntaje > 21):
                    _jug.darGanancia(2)
                    _jug.enviarMensaje("Felicitaciones! Ganaste!")
                elif puntaje == _jug.manoActual.obtenerPuntaje():
                    _jug.darGanancia(1)
                    _jug.enviarMensaje("es un empate, recuperaste lo aposado!")
                else:
                    _jug.enviarMensaje("Perdiste contra la banca!")
            self.segundosTotales = 0
            self.jugadorActual = None
            self.empezarTimer()

        else:
            self.jugadorActualIndice += 1
            self.jugadorActual = self.jugadores[self.jugadoresActivos[self.jugadorActualIndice]]
        self.notificarJugadoresActivos("es el turno de " + self.jugadorActual.usuario.nombre)

    """
        Maneja la petición de una carta, y el escenario de perdida en caso de que se exceda de los puntos.
    """
    def pedir(self, usuario):
        _jugador = self._obtenerJugador(usuario)
        if self._esJugadorActual(usuario) == False:
            _jugador.enviarMensaje("No es tu turno")
        else:
            proxima = self.mazo.proximaCarta()
            puntajeTotal = _jugador.pedir(proxima)
            if puntajeTotal > 21:
                _jugador.enviarMensaje("Finalizo tu mano con un puntaje de " + _jugador.manoActual.obtenerDescripcionCompleta())
                _jugador.marcarComoPerdedor()
                self.rotarJugador()

    """
        Maneja la petición de plantarse
    """
    def plantarse(self, usuario):
        _jugador = self._obtenerJugador(usuario)
        if not self.jugadorActual.usuario.nombre  == usuario:
            _jugador.enviarMensaje("No es tu turno")
        else:
            self.jugadorActual.plantarse()
            self.rotarJugador()

    """
        Maneja la petición de doblar la apuesta. Solo puede hacerlo si tiene el dinero suficiente
    """
    def doblar(self, usuario):
        _jugador = self._obtenerJugador(usuario)
        if not self.jugadorActual.usuario.nombre  == usuario:
            _jugador.enviarMensaje("No es tu turno")
        else:
            try:
                self.jugadorActual.doblarApuesta()
                proxima = self.mazo.proximaCarta()
                puntajeTotal = self.jugadorActual.pedir(proxima)
                if puntajeTotal > 21:
                    self.jugadorActual.marcarComoPerdedor()
                    self.jugadorActual.enviarMensaje("Finalizaste con un puntaje de " + _jugador.manoActual.obtenerDescripcionCompleta())
                else:
                    self.jugadorActual.plantarse()
                self.rotarJugador()    
            except DineroInsuficiente:
                _jugador.enviarMensaje("Dinero insuficiente")        

        





            


