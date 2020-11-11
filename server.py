import json
import os
import socket
from _thread import *
import threading
import traceback
import codigoMesaje
import sqlite3
from pathlib import Path

from blackjack import Blackjack

clientes = []
diccionario = {}

"""
    La clase usuario representa la relacion entre un nombre (identificador unico del usuario) y el socket asociado al mismo.
"""
class Usuario:
    def __init__(self, socket):
        self.nombre = None
        self.socket = socket
        self.dinero = 0
        self.idioma = "es"

    def enviarData(self, data):
        try:
            self.socket.send(data.encode())
        except:
            pass

    def enviarMensaje(self, mensajeArg, comandos = [], jugadores = [], banca = [], mano = [], finalizado = False, pCodigoMensaje =codigoMesaje.NORMAL):
        mensaje = ""
        _comm = comandos.copy()
        _comm.append("mensaje")
        if self.nombre == None:
            _comm.append("soy")
        elif self.dinero == 0:
            _comm.append("ingresar")
        mensaje += ("comandos:"+"#".join(_comm))
        if len(jugadores) > 0:
            mensaje += ("|jugadores:"+"#".join(jugadores))
        if len(banca) > 0:
            mensaje += ("|banca:"+",".join(banca))
        if len(mano) > 0:
            mensaje += ("|mano:"+",".join(mano))
        mensaje += "|partida:" + str(finalizado)
        mensaje += "|codigo:" + pCodigoMensaje
        mensaje += ("|mensaje:" + mensajeArg + "\n")
        self.enviarData(mensaje)

"""
    La clase ejecutor esta implementada con un patron strategy. Los comandos a ejecutar implementan la misma interfaz
    y dependiendo del contexto (un comando en este caso) elegimos que estrategia ejecutar.
"""
class Ejecutor:

    def __init__(self):
        self.comandos = {
            "soy": comIdentificarUsuario,
            "estadisticas": comJuegoComando,
            "doblar": comJuegoComando,
            "ingresar": comIngresarDinero,
            "iniciar": comJuegoComando,
            "apostar": comJuegoComando,
            "mensaje": comJuegoComando,
            "pedir": comJuegoComando,
            "plantarse": comJuegoComando
        }

    def ejecutar(self, comando, argumentos, socket, juego, cliente):
        ejecutorComando = self.comandos.get(comando)
        if ejecutorComando == None:
            return cliente.enviarMensaje(diccionario[cliente.idioma]["comandoDesconocido"])
        if comando != "soy" and cliente.nombre == None:
            return cliente.enviarMensaje(diccionario[cliente.idioma]["errorFaltaIdentificarse"])
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
        return juego.ingresarDinero(cliente.nombre, argumentos[0])
    if nombreComando == "iniciar":
        return juego.iniciarPartida(cliente.nombre,)
    if nombreComando == "apostar":
        return juego.apostar(cliente.nombre, argumentos[0])
    if nombreComando == "doblar":
        return juego.doblar(cliente.nombre)
    if nombreComando == "pedir":
        return juego.pedir(cliente.nombre)
    if nombreComando == "plantarse":
        return juego.plantarse(cliente.nombre)
    if nombreComando == "estadisticas":
        return juego.obtenerEstadisticas()
    if nombreComando == "mensaje":
        return juego.enviarMensaje(cliente.nombre, " ".join(argumentos))

"""
    El comando <soy> es para que el usuario se identifique
"""
def comIdentificarUsuario(nombreComando, argumentos, socket, juego, cliente):
    if (cliente.nombre == None):
        for d in diccionario:
            if diccionario[d]["banca"] == argumentos[0]:
                cliente.enviarMensaje(mensajeArg=diccionario[cliente.idioma]["errorNombreIgualBanca"], pCodigoMensaje=codigoMesaje.ALIAS_RECHAZADO)
                return

        cliente.nombre = argumentos[0]
        cliente.idioma = argumentos[1] if len(argumentos) > 1 else "es"
        cliente.enviarMensaje(mensajeArg=diccionario[cliente.idioma]["ingresarSaldo"], pCodigoMensaje=codigoMesaje.ALIAS_ACEPTADO)
    else:
        socket.send(diccionario[cliente.idioma]["errorYaTeConozco"].replace("{0}", cliente.nombre).replace("{1}", argumentos[0]) + "\n")

"""
    El comando <ingresar> es para ingresar dinero a la cuenta
"""
def comIngresarDinero(nombreComando, argumentos, socket, juego, cliente):
    monto = int(argumentos[0])
    if monto <= 0:
        cliente.enviarMensaje(diccionario[cliente.idioma]["ingresarMontoMayorCero"])
    else:
        cliente.dinero += monto
        juego.agregarJugador(cliente)

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
    usuario.enviarMensaje(diccionario[usuario.idioma]["bienvenidoAlJuego"])
    ejecutor = Ejecutor()
    while True:
        try:
            mensajeRecibido = cliente.recv(1024)
            tokens = mensajeRecibido.decode("utf-8").split()
            comando = tokens[0] if len(tokens) > 0 else mensajeRecibido
            argumentos = tokens[1:] if len(tokens) > 0 else []
            ejecutor.ejecutar(comando, argumentos, cliente, bg, usuario)
        except Exception as e:
            traceback.print_exc()
            if usuario.nombre != None:
                bg.removerJugador(usuario.nombre)
            break



"""
    La funcion iniciarServidor inicializar la escucha en el puerto 3030 y configura las entidades necesarias (como el coordinador de juego de BlackJack).
    Acepta las conexiones entrantes, y llama a inicializarCliente en un nuevo threado.
"""
def iniciarServidor():
    files = os.listdir("lenguaje")
    for f in files:
        with open(os.path.join("lenguaje", f)) as json_file:
            name = Path(f).resolve().stem
            diccionario[name] = json.load(json_file)



    puerto = 3039
    blackGame = Blackjack(diccionario)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', puerto))
    print(crearMensajeLog("Socket bindeado"))
    sock.listen(5)
    print(crearMensajeLog("Socket escuchando"))
    while True:
        cliente, direccionCliente = sock.accept()
        print(cliente)
        print(crearMensajeLog("Nuevo jugador desde: " + direccionCliente[0]))
        start_new_thread(inicializarCliente, (cliente, blackGame))
    sock.close()



if __name__ == "__main__":
    iniciarServidor()
