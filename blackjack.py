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

    def __init__(self, pDiccionario):
        self.manejadorDB = ManejadorDB(False)
        self.jugadoresTotales = []
        self.jugadoresJugando = []
        self.jugadorActualIndice = None
        self.rondaActiva = False
        self.interrumpirTimer = False
        self.jugadorActual = None
        self.timerIniciado = False
        self.banca = Banca(pDiccionario)
        self.segundosTotales = 0
        self.mazo = None
        self.diccionario = pDiccionario
        self.finalizado = False

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
        if jugadorSeleccionado is not None:
            if esJugadorActivo is True:
                comandos.append("pedir")
                comandos.append("plantarse")
                comandos.append("doblar")
                if len(jugadorSeleccionado.manoActual.cartas) == 2:
                    if jugadorSeleccionado.manoActual.cartas[0].valor == jugadorSeleccionado.manoActual.cartas[1].valor:
                        comandos.append("separar")
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

        for d in self.diccionario:
            jugadoresLenguaje = self.obtenerJugadoresIdioma(self.jugadoresTotales, d)
            self.notificarJugadores(jugadoresLenguaje, self.diccionario[d]["usuarioAbandono"].replace("{0}",usuario))


    def obtenerEstadoJugadores(self):
        estados = []
        manoDesc = None
        puntaje = None
        for i in range(len(self.jugadoresJugando)):
            jugActual = self.jugadoresJugando[i]
            if not jugActual.manoActual == None:
                manoDesc = jugActual.manoActual.obtenerValores()
                puntaje = jugActual.manoActual.obtenerPuntaje()

            estadoJugador = "{" + jugActual.usuario.nombre + ", " + str(jugActual.usuario.dinero) + ", " + jugActual.estadoActual
            if not manoDesc == None:
                estadoJugador = estadoJugador + ", " + "[" + ",".join(manoDesc) + "]"
                estadoJugador = estadoJugador + ", " + str(puntaje)

            estados.append(estadoJugador + "}")
        return estados

    def obtenerJugadoresIdioma(self, jugadores, idioma):
        jugadoresIdioma = []
        for j in jugadores:
            if j.usuario.idioma == idioma:
                jugadoresIdioma.append(j)
        return jugadoresIdioma

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
            banca = [("{" + ",".join(bancaValores) + "}" + "#" + str(bancaPuntaje))]
        for jug in range(len(jugadores)):
            jugSel = jugadores[jug]
            comandos = self.calcularComandos(jugSel.usuario.nombre)
            jugadores[jug].enviarMensaje(mensaje, comandos, jugadoresEstados, banca, [], self.finalizado)

    def notificarJugador(self, jugador, mensaje):
        self._notificarJugadores([jugador], mensaje)

    """
        Esta funcion envia un mensaje a todos los jugadores, activos o no.
    """
    def notificarJugadores(self, jugadores, mensaje):
        #self._notificarJugadores(self.jugadoresTotales, mensaje)
        self._notificarJugadores(jugadores, mensaje)

    """
        Esta funcion envia un mensaje a los jugadores que estan participando de la ronda.
    """
    def notificarJugadoresActivos(self, jugadores, mensaje):
        #self._notificarJugadores(self.jugadoresJugando, mensaje)
        self._notificarJugadores(jugadores, mensaje)

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
        self.finalizado = False
        segundosRestantes = 5-self.segundosTotales
        if segundosRestantes % 10 == 0:
            for d in self.diccionario:
                jugadoresLenguaje = self.obtenerJugadoresIdioma(self.jugadoresTotales, d)
                self.notificarJugadores(jugadoresLenguaje, self.diccionario[d]["timerEmpiezaElJuego"].replace("{0}", str(segundosRestantes)))
            #self.notificarJugadores("empieza el juego en " + str(segundosRestantes) + " segundos")
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
                self.notificarJugador(self.jugadoresJugando[j], self.diccionario[self.jugadoresJugando[j].usuario.idioma]["solicitarApuesta"])
                

    """
        Cuando se conecta un usuario nuevo, esta funcion decide si colocarlo en la lista de espera o no.
    """
    def decidirUsuario(self, jugador):
        if self.rondaActiva == True:
            self.notificarJugador(jugador, self.diccionario[jugador.usuario.idioma]["hayRondaActiva"])
        else:
            if self.timerIniciado == False:
                self.notificarJugador(jugador, self.diccionario[jugador.usuario.idioma]["iniciarCuentaRegresiva"])
                self.empezarTimer()
            else:
                self.notificarJugador(jugador, self.diccionario[jugador.usuario.idioma]["finalizacionCuentaRegresiva"])

    """
        Esta funcion maneja la peticion de agregar un jugador al juego.
        Mover el check del nombre de usuario a la funcion principal.
    """
    def agregarJugador(self, usuario):
        jug = self.obtenerJugadorTotal(usuario.nombre)
        if jug == None:
            self.interrumpirTimer = True
            nuevoJugador = Jugador(usuario, self.diccionario)
            nuevoJugador.enviarMensaje(self.diccionario[usuario.idioma]["bienvenido"] + usuario.nombre + "")
            self.jugadoresTotales.append(nuevoJugador)
            for d in self.diccionario:
                jugadoresLenguaje = self.obtenerJugadoresIdioma(self.jugadoresTotales, d)
                self.notificarJugadores(jugadoresLenguaje, self.diccionario[d]["jugadorSeUnio"].replace("{0}", usuario.nombre))
            self.decidirUsuario(nuevoJugador)
        else:
            #self.notificarJugadores(self.diccionario[usuario.idioma]["jugadorFondeo"].replace("{0}", usuario.nombre))
            for d in self.diccionario:
                jugadoresLenguaje = self.obtenerJugadoresIdioma(self.jugadoresTotales, d)
                self.notificarJugadores(jugadoresLenguaje, self.diccionario[d]["jugadorFondeo"].replace("{0}", usuario.nombre))
    
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
        self.notificarJugadores(self.jugadoresTotales, mensaje)

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

            #self.notificarJugadores("La banca tiene " + self.banca.mano.obtenerDescripcionCompleta())
            for d in self.diccionario:
                jugadoresLenguaje = self.obtenerJugadoresIdioma(self.jugadoresTotales, d)
                descripcionManoIdioma = self.banca.mano.obtenerDescripcionCompleta(d)
                self.notificarJugadores(jugadoresLenguaje, self.diccionario[d]["bancaTiene"].replace("{0}", descripcionManoIdioma))

            self.jugadorActualIndice = 0
            self.jugadorActual = self.jugadoresJugando[0]
            self.jugadorActual.estadoActual = "activo"
            #self.notificarJugadores("es el turno de " + self.jugadorActual.usuario.nombre)
            for d in self.diccionario:
                jugadoresLenguaje = self.obtenerJugadoresIdioma(self.jugadoresTotales, d)
                self.notificarJugadores(jugadoresLenguaje, self.diccionario[d]["esTurnoDe"].replace("{0}", self.jugadorActual.usuario.nombre))


    """
        Esta funcion maneja la peticion de apuesta de los usuarios.
    """
    def apostar(self, usuario, monto):
        _jugador = self._obtenerJugador(usuario)
        try:
            _jugador.apostar(monto)
            self._deberiaEmpezar()
        except DineroInsuficiente:
            self.notificarJugador(_jugador, self.diccionario[_jugador.usuario.idioma]["dineroInsuficiente"])
        except ApuestaRealizada:
            self.notificarJugador(_jugador, self.diccionario[_jugador.usuario.idioma]["apuestaYaRealizada"])

    """
        Funcion que rota los jugadores y, en caso que ya no queden mas para rotar, hace jugar a la banca.
    """
    def rotarJugador(self):
        if len(self.jugadoresJugando) == (self.jugadorActualIndice+1):
            self.jugadorActual = None
            #self.notificarJugadoresActivos("Ahora jugara la banca")
            for d in self.diccionario:
                jugadoresLenguaje = self.obtenerJugadoresIdioma(self.jugadoresJugando, d)
                self.notificarJugadoresActivos(jugadoresLenguaje, self.diccionario[d]["juegaLaBanca"])

            self.banca.mano.mostrarTodas()
            #self.notificarJugadoresActivos("La banca mostrara su carta oculta")
            for d in self.diccionario:
                jugadoresLenguaje = self.obtenerJugadoresIdioma(self.jugadoresJugando, d)
                self.notificarJugadoresActivos(jugadoresLenguaje, self.diccionario[d]["bancaMuestraCartaOculta"])

            #self.notificarJugadoresActivos("La banca tiene: " + self.banca.mano.obtenerDescripcionCompleta())
            for d in self.diccionario:
                jugadoresLenguaje = self.obtenerJugadoresIdioma(self.jugadoresJugando, d)
                self.notificarJugadoresActivos(jugadoresLenguaje, self.diccionario[d]["bancaTiene"].replace("{0}", self.banca.mano.obtenerDescripcionCompleta(d)))

            while self.banca.mano.obtenerPuntaje() <= 16:
                proxCarta = self.mazo.proximaCarta()
                self.banca.mano.agregarCarta(proxCarta)

                for d in self.diccionario:
                    jugadoresLenguaje = self.obtenerJugadoresIdioma(self.jugadoresJugando, d)
                    self.notificarJugadoresActivos(jugadoresLenguaje, self.diccionario[d]["bancaTiene"].replace("{0}",
                                                                                                                self.banca.mano.obtenerDescripcionCompleta(
                                                                                                                    d)))
            puntaje = self.banca.mano.obtenerPuntaje()
            for jugador in range(len(self.jugadoresJugando)):
                _jug = self.jugadoresJugando[jugador]
                if _jug.estadoActual == "finalizado_pendiente" and (_jug.manoActual.obtenerPuntaje() > puntaje or puntaje > 21):
                    _jug.darGanancia(2)
                    _jug.marcarComoGanador()
                    _jug.enviarMensaje(self.diccionario[_jug.usuario.idioma]["ganador"])
                elif puntaje == _jug.manoActual.obtenerPuntaje():
                    _jug.darGanancia(1)
                    _jug.marcarComoEmpate()
                    _jug.enviarMensaje(self.diccionario[_jug.usuario.idioma]["empate"])
                else:
                    _jug.marcarComoPerdedor()
                    _jug.enviarMensaje(self.diccionario[_jug.usuario.idioma]["perdedor"])

            self.finalizado = True
            for d in self.diccionario:
                jugadoresLenguaje = self.obtenerJugadoresIdioma(self.jugadoresJugando, d)
                self.notificarJugadoresActivos(jugadoresLenguaje, self.diccionario[d]["partidaFinalizada"])

            self.manejadorDB.registrarPartida(self.jugadoresJugando)
            self.segundosTotales = 0
            self.jugadorActual = None
            self.empezarTimer()

        else:
            self.jugadorActualIndice += 1
            self.jugadorActual = self.jugadoresJugando[self.jugadorActualIndice]
            self.jugadorActual.estadoActual = "activo"
            #self.notificarJugadoresActivos("es el turno de " + self.jugadorActual.usuario.nombre)
            for d in self.diccionario:
                jugadoresLenguaje = self.obtenerJugadoresIdioma(self.jugadoresJugando, d)
                self.notificarJugadoresActivos(jugadoresLenguaje, self.diccionario[d]["esTurnoDe"].replace("{0}", self.jugadorActual.usuario.nombre))


    """
        Maneja la petición de una carta, y el escenario de perdida en caso de que se exceda de los puntos.
    """
    def pedir(self, usuario):
        _jugador = self._obtenerJugador(usuario)
        if self._esJugadorActual(usuario) == False:
            self.notificarJugador(_jugador, self.diccionario[usuario.idioma]["noEsTurno"])
        else:
            proxima = self.mazo.proximaCarta()
            puntajeTotal = _jugador.pedir(proxima)
            for d in self.diccionario:
                jugadoresLenguaje = self.obtenerJugadoresIdioma(self.jugadoresJugando, d)
                self.notificarJugadoresActivos(jugadoresLenguaje, self.diccionario[d]["puntajeObtenido"].replace("{0}", _jugador.usuario.nombre).replace("{1}", str(puntajeTotal)))

            if puntajeTotal > 21:
                for d in self.diccionario:
                    jugadoresLenguaje = self.obtenerJugadoresIdioma(self.jugadoresJugando, d)
                    self.notificarJugadoresActivos(jugadoresLenguaje, self.diccionario[d]["jugadorPerdio"].replace("{0}", self.jugadorActual.usuario.nombre).replace("{1}", _jugador.manoActual.obtenerDescripcionCompleta(d)))
                _jugador.marcarComoPerdedor()
                self.rotarJugador()

    """
        Maneja la petición de plantarse
    """
    def plantarse(self, usuario):
        _jugador = self._obtenerJugador(usuario)
        if not self.jugadorActual.usuario.nombre == usuario:
            self.notificarJugador(_jugador, self.diccionario[usuario.idioma]["noEsTurno"])
        else:
            self.jugadorActual.plantarse()
            self.rotarJugador()

    """
        Maneja la petición de doblar la apuesta. Solo puede hacerlo si tiene el dinero suficiente
    """
    def doblar(self, usuario):
        _jugador = self._obtenerJugador(usuario)
        if not self.jugadorActual.usuario.nombre  == usuario:
            self.notificarJugador(_jugador, self.diccionario[usuario.idioma]["noEsTurno"])
        else:
            try:
                self.jugadorActual.doblarApuesta()
                proxima = self.mazo.proximaCarta()
                puntajeTotal = self.jugadorActual.pedir(proxima)
                if puntajeTotal > 21:
                    self.jugadorActual.marcarComoPerdedor()
                    #self.notificarJugadores(self.jugadorActual.usuario.nombre + " perdio con un puntaje de " + _jugador.manoActual.obtenerDescripcionCompleta())
                    for d in self.diccionario:
                        jugadoresLenguaje = self.obtenerJugadoresIdioma(self.jugadoresJugando, d)
                        self.notificarJugadoresActivos(jugadoresLenguaje, self.diccionario[d]["jugadorPerdio"].replace("{0}", self.jugadorActual.usuario.nombre).replace("{1}", _jugador.manoActual.obtenerDescripcionCompleta(d)))
                else:
                    self.jugadorActual.plantarse()
                self.rotarJugador()    
            except DineroInsuficiente:
                self.notificarJugador(_jugador, self.diccionario[usuario.idioma]["dineroInsuficiente"])

    def enviarMensaje(self, nombreUsuario, mensaje):
        self.notificarJugadores("[" + nombreUsuario + "] " + mensaje)

        





            


