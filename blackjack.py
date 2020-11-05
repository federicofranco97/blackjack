from threading import Timer
from mazo import Mazo, Carta, Mano
from excepciones import NombreUsado, DineroInsuficiente, ApuestaRealizada, JugadorInexistente, ComandoNoPermitido
from jugador import Jugador, Banca
from sql import ManejadorDB
import copy

"""
    Coordinador del juego. Se encarga de todo aquello que excede los limites del jugador en si mismo. Coordina las rondas y mantiene
    el estado general del kjuego.
"""

class Blackjack():

    def __init__(self):
        self.manejadorDB = ManejadorDB(False)
        self.jugadoresTotales = []
        self.jugadoresJugando = []
        self.jugadorActualIndice = None
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

    def obtenerJugadorActivo(self, nombreUsuario):
        for i in range(len(self.jugadoresJugando)):
            if self.jugadoresJugando[i].usuario.nombre == nombreUsuario:
                return self.jugadoresJugando[i]
        return None

    def obtenerJugadorTotal(self, nombreUsuario):
        print("Usuario buscador: " + nombreUsuario)
        for i in range(len(self.jugadoresTotales)):
            print(self.jugadoresTotales[i].usuario.nombre)
            if self.jugadoresTotales[i].usuario.nombre == nombreUsuario:
                return self.jugadoresTotales[i]
        return None


    def calcularComandos(self, nombreUsuario):
        comandos = []
        jugadorSeleccionado = self.obtenerJugadorTotal(nombreUsuario)
        esJugadorActivo = self._esJugadorActual(nombreUsuario)
        if not jugadorSeleccionado == None:
            if esJugadorActivo == True:
                comandos.append("pedir")
                comandos.append("plantarse")
                comandos.append("doblar")
            if jugadorSeleccionado.estadoActual == "apuesta_pendiente":
                comandos.append("apostar")
        return comandos

    def removerJugador(self, usuario):
        for i in range(len(self.jugadoresTotales)):
            if self.jugadoresTotales[i].usuario.nombre == usuario:
                del self.jugadoresTotales[i]
        for j in range(len(self.jugadoresJugando)):
            if self.jugadoresJugando[j].usuario.nombre == usuario:
                del self.jugadoresJugando[j]
        if not self.jugadorActual == None:
            if self.jugadorActual.usuario.nombre == usuario:
                self.jugadorActualIndice = self.jugadorActualIndice-1
                self.rotarJugador()
        self.notificarJugadores("el usuario " + usuario + " abandono la sala")

    def obtenerEstadoJugadores(self):
        estados = []
        manoDesc = None
        puntaje = None
        for i in range(len(self.jugadoresJugando)):
            jugActual = self.jugadoresJugando[i]
            if not jugActual.manoActual == None:
                manoDesc = jugActual.manoActual.obtenerValores()
                puntaje = jugActual.manoActual.obtenerPuntaje()

            #estadoJugador = "{" + jugActual.usuario.nombre + "," + str(jugActual.usuario.dinero) + "," + jugActual.estadoActual
            #if not manoDesc == None:
            #    estadoJugador = estadoJugador + "," + "[" + ",".join(manoDesc) + "]"
            #    estadoJugador = estadoJugador + "," + str(puntaje)

            estadoJugador = "{" + jugActual.usuario.nombre + ", " + str(jugActual.usuario.dinero) + ", " + jugActual.estadoActual
            if not manoDesc == None:
                estadoJugador = estadoJugador + ", " + "[" + ",".join(manoDesc) + "]"
                estadoJugador = estadoJugador + ", " + str(puntaje)

            estados.append(estadoJugador + "}")
        return estados

    """
        Esta funcion se utiliza para enviar un mensaje a una lista de jugadores. Es una funcion pseudo-privada, no deberia ser llamada directamente, sino
        a traves de notificarJugadores o notificarJugadoresActivos o notificarJugador.
    """
    def _notificarJugadores(self, jugadores, mensaje):
        banca = []
        jugadoresEstados = self.obtenerEstadoJugadores()
        if not self.banca.mano == None:
            bancaValores = self.banca.mano.obtenerValores()
            bancaPuntaje = self.banca.mano.obtenerPuntaje()
            banca = [("{"+ ",".join(bancaValores) + "}" + "#" + str(bancaPuntaje))]
        for jug in range(len(jugadores)):
            jugSel = jugadores[jug]
            comandos = self.calcularComandos(jugSel.usuario.nombre)
            jugadores[jug].enviarMensaje(mensaje, comandos, jugadoresEstados, banca)

    def notificarJugador(self, jugador, mensaje):
        self._notificarJugadores([jugador], mensaje)

    """
        Esta funcion envia un mensaje a todos los jugadores, activos o no.
    """
    def notificarJugadores(self, mensaje):
        self._notificarJugadores(self.jugadoresTotales, mensaje)

    """
        Esta funcion envia un mensaje a los jugadores que estan participando de la ronda.
    """
    def notificarJugadoresActivos(self, mensaje):
        self._notificarJugadores(self.jugadoresJugando, mensaje)

    """
        Obtiene la referencia de un jugador para utilizarlo.
    """
    def _obtenerJugador(self, nombre):
        for i in range(len(self.jugadoresTotales)):
            if self.jugadoresTotales[i].usuario.nombre == nombre:
                return self.jugadoresTotales[i]
        raise JugadorInexistente()

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
        segundosRestantes = 5-self.segundosTotales
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
            self.jugadoresJugando = self.jugadoresTotales.copy()
            self.banca.iniciarTurno()
            for i in range(len(self.jugadoresJugando)):
                self.jugadoresJugando[i].esperandoApuesta()
            for j in range(len(self.jugadoresJugando)):
                self.notificarJugador(self.jugadoresJugando[j], "ingresa tu apuesta")
                

    """
        Cuando se conecta un usuario nuevo, esta funcion decide si colocarlo en la lista de espera o no.
    """
    def decidirUsuario(self, jugador):
        if self.rondaActiva == True:
            self.notificarJugador(jugador, "Hay una ronda activa, una vez finalizada se te unirá automaticamente. Puedes irte de la espera cerrando la conexion.")
        else:
            if self.timerIniciado == False:
                self.notificarJugador(jugador, "Iniciaremos cuenta regresiva para iniciar el juego")
                self.empezarTimer()
            else:
                self.notificarJugador(jugador, "Una vez finalizada la cuenta regresiva, comenzara la partida")

    """
        Esta funcion maneja la peticion de agregar un jugador al juego.
        Mover el check del nombre de usuario a la funcion principal.
    """
    def agregarJugador(self, usuario):
        jug = self.obtenerJugadorTotal(usuario.nombre)
        if jug == None:
            self.interrumpirTimer = True
            nuevoJugador = Jugador(usuario)
            nuevoJugador.enviarMensaje("Bienvenido " + usuario.nombre + "")
            self.jugadoresTotales.append(nuevoJugador)
            self.notificarJugadores(usuario.nombre + " se unio al juego")
            self.decidirUsuario(nuevoJugador)
        else:
            self.notificarJugadores(usuario.nombre + " ha ingresado dinero")
    
    """
        Devuelve la cantidad de jugadores
    """
    def obtenerEstadisticas(self):
        mensaje = ""
        (estadJugadores, estadCartas) = self.manejadorDB.obtenerEstadisticas()
        for fila in estadJugadores:
            mensaje += ("Jugador: " + fila[0] + ". Ganadas: " + str(fila[1]) + ". Empatadas: " + str(fila[2]) + ". Perdidas: " + str(fila[3]) + "\n")
        for f in estadCartas:
            mensaje += ("Carta: " + f[0] + ". Cantidad de aparaciones: " + str(f[1]) + "\n")
        self.notificarJugadores(mensaje)

    """
        Funciona que chequea si el juego debe comenzar, es decir, si el resto de los participanes ya hizo una apuesta.
        De haber hecho todas las apuestas, se reparten las primeras cartas.
    """
    def _deberiaEmpezar(self):
        apuestasPendientes = 0
        for i in range(len(self.jugadoresJugando)):
            if self.jugadoresJugando[i].apuestaInicial == None:
                apuestasPendientes += 1
        if apuestasPendientes == 0:
            for ronda in range(2):
                for indiceAct in range(len(self.jugadoresJugando)):
                    jugadorActual = self.jugadoresJugando[indiceAct]
                    proximaCarta = self.mazo.proximaCarta()
                    jugadorActual.pedir(proximaCarta)
                cartaBanca = self.mazo.proximaCarta()
                if ronda == 1:
                    cartaBanca.visible = False
                self.banca.mano.agregarCarta(cartaBanca)
            self.notificarJugadores("La banca tiene " + self.banca.mano.obtenerDescripcionCompleta())
            self.jugadorActualIndice = 0
            self.jugadorActual = self.jugadoresJugando[0]
            self.jugadorActual.estadoActual = "activo"
            self.notificarJugadores("es el turno de " + self.jugadorActual.usuario.nombre)


    """
        Esta funcion maneja la peticion de apuesta de los usuarios.
    """
    def apostar(self, usuario, monto):
        _jugador = self._obtenerJugador(usuario)
        try:
            _jugador.apostar(monto)
            self._deberiaEmpezar()
        except DineroInsuficiente:
            self.notificarJugador(_jugador, "No tienes el dinero suficiente")
        except ApuestaRealizada:
            self.notificarJugador(_jugador, "Ya realizaste la apuesta de esta mano")

    """
        Funcion que rota los jugadores y, en caso que ya no queden mas para rotar, hace jugar a la banca.
    """
    def rotarJugador(self):
        if len(self.jugadoresJugando) == (self.jugadorActualIndice+1):
            self.jugadorActual = None
            self.notificarJugadoresActivos("ahora jugara la banca")
            self.banca.mano.mostrarTodas()
            self.notificarJugadoresActivos("la banca mostrar su carta oculta")
            self.notificarJugadoresActivos("la banca tiene: " + self.banca.mano.obtenerDescripcionCompleta())
            while self.banca.mano.obtenerPuntaje() <= 16:
                proxCarta = self.mazo.proximaCarta()
                self.banca.mano.agregarCarta(proxCarta)
                self.notificarJugadoresActivos("la banca tiene: " + self.banca.mano.obtenerDescripcionCompleta())
            puntaje = self.banca.mano.obtenerPuntaje()
            for jugador in range(len(self.jugadoresJugando)):
                _jug = self.jugadoresJugando[jugador]
                if _jug.estadoActual == "finalizado_pendiente" and (_jug.manoActual.obtenerPuntaje() > puntaje or puntaje > 21):
                    _jug.darGanancia(2)
                    _jug.marcarComoGanador()
                    _jug.enviarMensaje("Felicitaciones! Ganaste!")
                elif puntaje == _jug.manoActual.obtenerPuntaje():
                    _jug.darGanancia(1)
                    _jug.marcarComoEmpate()
                    _jug.enviarMensaje("es un empate, recuperaste lo aposado!")
                else:
                    _jug.marcarComoPerdedor()
                    _jug.enviarMensaje("Perdiste contra la banca!")
            self.manejadorDB.registrarPartida(self.jugadoresJugando)
            self.segundosTotales = 0
            self.jugadorActual = None
            self.empezarTimer()

        else:
            self.jugadorActualIndice += 1
            self.jugadorActual = self.jugadoresJugando[self.jugadorActualIndice]
            self.jugadorActual.estadoActual = "activo"
            self.notificarJugadoresActivos("es el turno de " + self.jugadorActual.usuario.nombre)

    """
        Maneja la petición de una carta, y el escenario de perdida en caso de que se exceda de los puntos.
    """
    def pedir(self, usuario):
        _jugador = self._obtenerJugador(usuario)
        if self._esJugadorActual(usuario) == False:
            self.notificarJugador(_jugador, "No es tu turno")
        else:
            proxima = self.mazo.proximaCarta()
            puntajeTotal = _jugador.pedir(proxima)
            self.notificarJugadores(_jugador.usuario.nombre + " ha obtenido " + str(puntajeTotal))
            if puntajeTotal > 21:
                self.notificarJugadores(self.jugadorActual.usuario.nombre + " perdio con un puntaje de " + _jugador.manoActual.obtenerDescripcionCompleta())
                _jugador.marcarComoPerdedor()
                self.rotarJugador()

    """
        Maneja la petición de plantarse
    """
    def plantarse(self, usuario):
        _jugador = self._obtenerJugador(usuario)
        if not self.jugadorActual.usuario.nombre  == usuario:
            self.notificarJugador(_jugador, "No es tu turno")
        else:
            self.jugadorActual.plantarse()
            self.rotarJugador()

    """
        Maneja la petición de doblar la apuesta. Solo puede hacerlo si tiene el dinero suficiente
    """
    def doblar(self, usuario):
        _jugador = self._obtenerJugador(usuario)
        if not self.jugadorActual.usuario.nombre  == usuario:
            self.notificarJugador(_jugador, "No es tu turno")
        else:
            try:
                self.jugadorActual.doblarApuesta()
                proxima = self.mazo.proximaCarta()
                puntajeTotal = self.jugadorActual.pedir(proxima)
                if puntajeTotal > 21:
                    self.jugadorActual.marcarComoPerdedor()
                    self.notificarJugadores(self.jugadorActual.usuario.nombre + " perdio con un puntaje de " + _jugador.manoActual.obtenerDescripcionCompleta())
                else:
                    self.jugadorActual.plantarse()
                self.rotarJugador()    
            except DineroInsuficiente:
                self.notificarJugador(_jugador, "No tienes el dinero suficiente")

        





            


