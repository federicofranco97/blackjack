import os
import random
import select
import socket
import sys
from _thread import *
import logging
import re
from datetime import date, datetime
import time

from pip._vendor.distlib.compat import raw_input

from gui import *
from guiViewModel import GuiViewModel

hayJugadoresEnEspera = False
hayPartidaEnCurso = True
sock = None

vm = GuiViewModel()
"""
    Metodo que escucha el socket del servidor y se dedica a imprimir los mensajes parseados que 
    recibe del servidor.
"""


def escucharServidor():
    while 1:
        try:
            data = sock.recv(4096)
            if not data:
                continue
            else:
                print(data)
                # Imprimo los mensajes del servidor
                mensajes = getMensajesServidor(data)
                for m in mensajes:
                    print(m)
                    mensajeParseado = parsearMensajeServidor(m)
                    if m.split("|")[0] == "mensaje":
                        vm.onMensajeEntrante(mensajeParseado)

            # time.sleep(1)
            #if random.randint(1, 4) == 1:
                #vm.onTurnoChanged("sebastian")

        except socket.timeout:
            mensajeError = "Se perdio la conexion con el servidor"
            print(mensajeError)
            vm.onMensajeEntrante(mensajeError)

def getMensajesServidor(mensajeRecibido):
    mensajes = mensajeRecibido.decode("utf-8").split("\n")
    return mensajes


"""
    Metodo que se dedica a parsear los mensajes que envia el servidor dependiendo de la modalidad de los mismos 
"""
def parsearMensajeServidor(mensajeRecibido):
    #mensajeBase = mensajeRecibido.decode("utf-8").split("|")
    mensajeBase = mensajeRecibido.split("|")
    comando = mensajeBase[0] if len(mensajeBase) > 0 else mensajeRecibido
    argumentos = mensajeBase[1:] if len(mensajeBase) > 0 else []
    if comando == "comandos" or comando == "status" or comando == "mensaje":
        formateo = str(argumentos).split("'")[1]
        return formateo.replace("\\n", "")
    elif comando == "partida":
        for x in argumentos:
            subcomando = str(x).split(":")[0]
            subargumentos = str(x).split(":")[1:]
            parsearSubComando(subcomando, subargumentos)
    else:
        return str(argumentos)


"""
    Metodo que se encarga de parsear los subcomandos que lleguen 
    a lo largo de la partida
"""
def parsearSubComando(subcom, args):
    if subcom == "mano":
        mano = parsearMano(args)
        puntaje = str(args).split('#')[1]
        return mano + " Y su puntaje es: " + puntaje
    elif subcom == "jugadores":
        listadoJugadores = str(args).split("#")
        return ""
    elif subcom == "":
        return ""
    else:
        return ""


def parsearJugadores(jugs):
    for j in jugs:
        props = (str(j).replace("{", "").replace("}", "")).split(",")


def parsearMano(arg):
    mensaje = "Su mano es: "
    manoparse = (str(arg).split('#')[0]).replace("{", "").replace("}", "")
    return mensaje + manoparse

def pedirCarta():
    print("pedir carta")
    comando = "pedir"
    sock.send(comando.encode())

def plantarse():
    print("me planto")
    comando = "plantarse"
    sock.send(comando.encode())

def doblar():
    print("doblar apuesta")

def separar():
    print("separar")

def fondear(monto):
    print("fondear " + monto)
    comando = "ingresar " + monto
    sock.send(comando.encode())

def apostar(monto):
    print("apostando " + monto)
    comando = "apostar " + monto
    sock.send(comando.encode())

def enviarMensaje(mensaje):
    print("enviando mensaje: " + mensaje)
    comando = "mensaje " + mensaje
    sock.send(comando.encode())


"""
    Metodo que inicializa el cliente, solicita los datos principales como ip del servidor,
    puerto, y luego de realizar la conexion pide el nombre de usuario
"""
def inicioCliente():
    print("Bienvenido al servidor de BlackJack")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(200)
    host = raw_input("Por favor ingresa la IP del servidor: ")
    port = raw_input("Por favor ingresa el puerto del servidor: ")
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, int(port)))
    except Exception as e:
        print("Ocurrio un error al conectarse con el servidor:", e)
        return
    print("Conectado, bienvenido al servidor!")

    start_new_thread(escucharServidor, ())
    start_new_thread(mostrarInterfaz, (vm,))
    while True:
        newMsg = sys.stdin.readline()
        sock.send(newMsg.encode())
    sock.close()


if __name__ == "__main__":

    vm.ee.on("pedirCartaEvent", pedirCarta)
    vm.ee.on("plantarseEvent", plantarse)
    vm.ee.on("separarEvent", separar)
    vm.ee.on("fondearEvent", fondear)
    vm.ee.on("apostarEvent", apostar)
    vm.ee.on("doblarEvent", doblar)



    inicioCliente()
    #start_new_thread(mostrarInterfaz, (vm,))
    while True:
        time.sleep(1)
        vm.Jugador = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        vm.Puntaje = 1000
        botones = []
        boton = random.randint(1, 10)
        if (boton == 1):
            botones.append("pedir")
        if (boton == 2):
            botones.append("plantarse")
        if (boton == 3):
            botones.append("doblar")
        if (boton == 4):
            botones.append("apostar")

        largo = random.randint(1, 20)
        mensaje = ""
        for i in range(largo):
            mensaje += chr(random.randint(97, 105))

        vm.onMensajeEntrante(mensaje)

        #vm.onRefreshButtons(botones)
        vm.MisCartas = [{ "P": random.randint(1, 4), "V": random.randint(1, 14)}, { "P": random.randint(1, 4), "V": random.randint(1, 14)}]

