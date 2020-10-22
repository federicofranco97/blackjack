import socket
from _thread import *
import threading
from blackjack import Blackjack

clientes = []
"""
    La clase usuario representa la relacion entre un nombre (identificador unico del usuario) y el socket asociado al mismo.
"""
class Usuario:
    def __init__(self, socket):
        self.nombre = None
        self.socket = socket

    def enviarMensaje(self, mensaje):
        self.socket.send(str(mensaje).encode())

"""
    La clase ejecutor esta implementada con un patron strategy. Los comandos a ejecutar implementan la misma interfaz
    y dependiendo del contexto (un comando en este caso) elegimos que estrategia ejecutar.
"""
class Ejecutor:

    def __init__(self):
        self.comandos = {
            "soy": comIdentificarUsuario,
            "estadisticas": comObtenerEstadisticas,
            "ingresar": comJuegoComando,
            "mensaje": comMensaje
        }

    def ejecutar(self, comando, argumentos, socket, juego, cliente):
        ejecutorComando = self.comandos.get(comando)
        print(str(comando))
        if ejecutorComando == None:
            return cliente.enviarMensaje("No conozco ese comando")
        if comando != "soy" and cliente.nombre == None:
            return cliente.enviarMensaje("Primero tenes que identificarte con el comando soy <nombre>")
        ejecutorComando(comando, argumentos, socket, juego, cliente)

"""
    Envia un mensaje a todos los usuarios del juego, esten jugando o no
"""

def comMensaje(nombreComando, argumentos, socket, juego, cliente):
    for _cliente in clientes:
        _cliente.enviarMensaje("["+cliente.nombre+"] " + " ".join(argumentos))

"""
    El comando ingresar se utiliza para fondear la cuenta del usuario, aunque en realidad
"""
def comJuegoComando(nombreComando, argumentos, socket, juego, cliente):
    if nombreComando == "ingresar":
        juego.ingresarDinero(cliente.nombre, argumentos[0])

"""
    El comando <soy> es para que el usuario s eidentifique
"""
def comIdentificarUsuario(nombreComando, argumentos, socket, juego, cliente):
    if (cliente.nombre == None):
        cliente.nombre = argumentos[0]
        juego.agregarJugador(cliente)
    else:
        socket.send("Ya te conozco. Te llamas " + cliente.nombre + ", no " + argumentos[0] + "\n")

"""
    El comando estadisticas se utiliza para obtener las estadisticas del juego
"""

def comObtenerEstadisticas(nombreComando, argumentos, socket, juego, cliente):
    estadisticas = juego.obtenerEstadisticas()
    cliente.enviarMensaje("Estadisticas: " + estadisticas + "\n")

"""
    Funcion auxiliar para debuggear
"""
def crearMensajeLog(mensaje):
    return ("[UBlackJack] " + mensaje)

"""
    La funcion inicializar cliente se encarga de hacer de puente entre el usuario y el coordinador de juego de BlackJack. Esta funcion esta dentro de un thread.
"""
def inicializarCliente(cliente, bg):
    usuario = Usuario(cliente)
    clientes.append(usuario)
    usuario.enviarMensaje("Bienvenido al juego. Ingresa tu nombre con el comando soy <nombre>.\n")
    ejecutor = Ejecutor()
    while True:
        mensajeRecibido = cliente.recv(1024)
        tokens = mensajeRecibido.decode("utf-8").split()
        comando = tokens[0] if len(tokens) > 0 else mensajeRecibido
        argumentos = tokens[1:] if len(tokens) > 0 else []
        ejecutor.ejecutar(comando, argumentos, cliente, bg, usuario)


"""
    La funcion iniciarServidor inicializar la escucha en el puerto 3030 y configura las entidades necesarias (como el coordinador de juego de BlackJack).
    Acepta las conexiones entrantes, y llama a inicializarCliente en un nuevo threado.
"""

def iniciarServidor():
    puerto = 3030
    blackGame = Blackjack()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("",puerto))
    print(crearMensajeLog("Socket bindeado"))
    sock.listen(5)
    print(crearMensajeLog("Socket escuchando"))
    while True:
        cliente, direccionCliente = sock.accept()
        print(crearMensajeLog("Nuevo jugador desde: " + direccionCliente[0]))
        start_new_thread(inicializarCliente, (cliente, blackGame))
    sock.close()

if __name__ == "__main__":
    iniciarServidor()
