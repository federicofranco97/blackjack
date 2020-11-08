"""
    Clase que representa a un jugador de blackjack
"""
from excepciones import DineroInsuficiente, ApuestaRealizada, ComandoNoPermitido
from mazo import Mano

class Jugador():

    def __init__(self, instanciaUsuario):
        self.usuario = instanciaUsuario
        self.apuestaInicial = None
        self.manoActual = None
        self.estadoActual = None

    def dineroSuficiente(self, monto):
        return self.usuario.dinero >= int(monto)

    def enviarMensaje(self, mensaje, comandos = [], jugadores = [], banca = [], mano = []):
        self.usuario.enviarMensaje("[Servidor] " + mensaje, comandos, jugadores, banca, mano)

    def esperandoApuesta(self):
        self.apuestaInicial = None
        self.estadoActual = "apuesta_pendiente"
        self.usuario.estadoActual = "apuesta_pendiente"
        self.manoActual = Mano()

    def darGanancia(self, multiplicador = 1):
        self.usuario.dinero = self.usuario.dinero + int(self.apuestaInicial*multiplicador)

    def doblarApuesta(self):
        if self.dineroSuficiente(self.apuestaInicial*2) == True:
            self.usuario.dinero = self.usuario.dinero-self.apuestaInicial
            self.apuestaInicial = self.apuestaInicial*2
        else:
            raise DineroInsuficiente()
            

    def apostar(self, monto):
        if not self.dineroSuficiente(monto):
            raise DineroInsuficiente()
        if self.apuestaInicial == None:
            self.apuestaInicial = int(monto)
            self.usuario.dinero = self.usuario.dinero - int(monto)
            self.enviarMensaje("hiciste una apuesta de $" + str(monto) + ". Tu saldo actual es de $" + str(self.usuario.dinero))
            self.estadoActual = "esperando_turno"
            self.manoActual = Mano()
        else:
            raise ApuestaRealizada()

    def pedir(self, carta):
        if self.apuestaInicial == None:
            raise ComandoNoPermitido()
        self.manoActual.agregarCarta(carta)
        puntajeMano = self.manoActual.obtenerPuntaje()
        return puntajeMano

    def marcarComoPerdedor(self):
        self.estadoActual = "finalizado_perdido"

    def marcarComoGanador(self):
        self.estadoActual = "finalizado_ganador"

    def marcarComoEmpate(self):
        self.estadoActual = "finalizado_empate"

    def plantarse(self):
        self.estadoActual = "finalizado_pendiente"


class Banca():

    def __init__(self, pDiccionario):
        self.mano = None
        self.diccionario = pDiccionario

    def iniciarTurno(self):
        self.mano = Mano(self.diccionario)

    def esBanca(self):
        return True