import ast
import os
import random
import select
import socket
import sys
import json
from _thread import *
import logging
import re
from datetime import date, datetime
import time

from pip._vendor.distlib.compat import raw_input
from gui import *
from guiViewModel import GuiViewModel
from ingresar import PantallaIngreso
from pantalla import PantallaPrincipal

usarGUI = True
hayJugadoresEnEspera = False
hayPartidaEnCurso = True
sock = None
lenguaje = "es"
diccionario = {}
vm = GuiViewModel()
estado = 0


# Iniciamos la GUI
def iniciarPantalla():
    pantallainicial = PantallaIngreso(vm)
    pantallainicial.mostrar()
    return


# Este metodo corre permanentemente escuchando el socket para recibir los mensajes del servidor
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

        except socket.timeout:
            mensajeError = lenguaje["conexionPerdida"]
            print(mensajeError)
            vm.onMensajeEntrante(mensajeError)

# Recibe todos los mensajes del socket, que entren en el buffer, y los parte para analizarlos posteriormente
def getMensajesServidor(mensajeRecibido):
    retorno = []
    mensajes = mensajeRecibido.decode("utf-8").split("\n")
    for m in mensajes:
        mensajesSplit = m.split('|')
        for m2 in mensajesSplit:
            retorno.append(m2)
    return retorno


# Recibe el mensaje y lo parsea, informando a la GUI o a consola segun corresponda
def parsearMensajeServidor(mensajeRecibido):
    mensajeBase = mensajeRecibido.split(":")
    comando = mensajeBase[0] if len(mensajeBase) > 0 else mensajeRecibido
    argumentos = mensajeBase[1:] if len(mensajeBase) > 0 else []

    if comando == "comandos":
        formateo = str(argumentos[0]).split("#")
        print("Comandos Posibles: " + " - ".join(formateo))
        vm.onRefreshButtons(formateo)
    elif comando == "mensaje":
        formateo = str(argumentos[0])
        if formateo == diccionario["ingresarSaldo"]:
            vm.onSoyAceptado()
        print(formateo)
        vm.onMensajeEntrante(formateo)
    elif comando == "status":
        formateo = str(argumentos).split("#")[1]
        return formateo.replace("\\n", "")
    elif comando == "banca":
        formateo = str(argumentos).split("#")
        vm.onPuntajeBancaChanged(formateo[1])
    elif comando == "jugadores":
        jugadores = argumentos[0].split("#")
        print("Lista jugadores")
        print(jugadores)
        vm.Jugadores = []
        estadisticas = ""
        for j in jugadores:
            datosJugador = j.replace("{", "[").replace("}", "]")
            datosJugador = datosJugador.strip('][').split(', ')
            print(datosJugador)
            print(datosJugador[4])
            if datosJugador[0] == vm.MiNombre:
                vm.MiPuntaje = datosJugador[4]
                vm.MiSaldo = datosJugador[1]
                vm.MiEstado = datosJugador[2]
                if len(datosJugador[3]) > 2:
                    tempCartas = datosJugador[3].strip('][').split(',')
                    vm.MisCartas = tempCartas
                else:
                    vm.MisCartas = []
                print(datosJugador[3])
                print(type(datosJugador[3]))
                vm.onEstadoChanged(vm.MiEstado)
                if vm.MiEstado == "activo":
                    if vm.Turno != vm.MiNombre:
                        vm.onTurnoChanged(vm.MiNombre)
            else:
                if datosJugador[2] == "activo":
                    vm.onTurnoChanged(datosJugador[0])
                estadisticas += datosJugador[0] + ' $' + datosJugador[1] + ' (' + datosJugador[2] + ')' + '\n'

        vm.onJugadoresRefreshed(estadisticas)
        print(estadisticas)
    else:
        return str(argumentos)


"""
Metodo que se encarga de parsear los subcomandos que lleguen a lo largo de la partida
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

# Envia el comando soy
def soy(usr):
    comando = "soy " + usr
    sock.send(comando.encode())
    vm.MiNombre = usr.replace('\n', '')


# Envia el pedido de carta
def pedirCarta():
    print("pedir carta")
    comando = "pedir"
    sock.send(comando.encode())

# Envia el pedido de plantarse
def plantarse():
    print("me planto")
    comando = "plantarse"
    sock.send(comando.encode())

# Envia la solicitud de doblar
def doblar():
    print("doblar apuesta")

# Envia la solicitud de split
def separar():
    print("separar")

# Envia el fondeo
def fondear(monto):
    print("fondear " + monto)
    comando = "ingresar " + monto
    sock.send(comando.encode())

# Envia la apuesta
def apostar(monto):
    print("apostando " + monto)
    comando = "apostar " + monto
    sock.send(comando.encode())

# Envia un mensaje por el socket
def enviarMensaje(mensaje):
    print("enviando mensaje: " + mensaje)
    comando = "mensaje " + mensaje
    sock.send(comando.encode())

# Se conecta al servidor con los parametros solicitados
def conectar(ip, puerto):
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, int(puerto)))
        start_new_thread(escucharServidor, ())
        estado = 1
        vm.onConnected()
    except Exception as e:
        print(diccionario["errorConexion"] + str(e))
        vm.onConnectError(diccionario["errorConexion"] + str(e))
        return False
    return True


def clienteConectado():
    pantalla = PantallaPrincipal(vm)
    pantalla.mostrar()


# Verifico que comando esta queriendo enviar en la consola y lo encapsulo en la funcion correspondiente (que tambien se invoca desde la GUI)
def analizarComandoEnviado(linea):
    try:
        comando = linea.split(" ")[0].replace('\n', '')
        if comando == "mensaje":
            argumentos = "".join(linea.split(" ")[1:])
        else:
            argumentos = " ".join(linea.split(" ")[1:])
        if comando == "soy":
            soy(argumentos)
        elif comando == "mensaje":
            enviarMensaje(" ".join(argumentos))
        elif comando == "ingresar":
            fondear(argumentos)
        elif comando == "apostar":
            apostar(argumentos)
        elif comando == "pedir":
            pedirCarta()
        elif comando == "plantarse":
            plantarse()
        elif comando == "separar":
            separar()
        elif comando == "doblar":
            doblar()
    except:
        print(diccionario["errorComando"])



#Metodo que inicializa el cliente, y decide si entrar en modo consola o con GUI
def inicioCliente():
    if not usarGUI:
        while True:
            host = raw_input(diccionario["solicitarIp"])
            port = raw_input(diccionario["solicitarPuerto"])
            if conectar(host, port):
                break
        print(diccionario["mensajeBienvenida"])


    if usarGUI:
        iniciarPantalla()
        while estado != 0:

            continue
            #start_new_thread(iniciarPantalla, (vm, ""))


    if not usarGUI:
        start_new_thread(escucharServidor, ())
        while True:
            newMsg = sys.stdin.readline()
            analizarComandoEnviado(newMsg)
        sock.close()



#Punto de entrada del Cliente
if __name__ == "__main__":
    with open(os.path.join("lenguaje", lenguaje + ".py")) as json_file:
        diccionario = json.load(json_file)

    vm.ee.on("pedirCartaEvent", pedirCarta)
    vm.ee.on("plantarseEvent", plantarse)
    vm.ee.on("separarEvent", separar)
    vm.ee.on("fondearEvent", fondear)
    vm.ee.on("apostarEvent", apostar)
    vm.ee.on("doblarEvent", doblar)
    vm.ee.on("enviarMensajeEvent", enviarMensaje)
    vm.ee.on("requestConnectionEvent", conectar)
    vm.ee.on("soyEvent", soy)
    vm.ee.on("enteredEvent", clienteConectado)
    inicioCliente()
