import ast
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
from pantalla import PantallaPrincipal

hayJugadoresEnEspera = False
hayPartidaEnCurso = True
sock = None

vm = GuiViewModel()
"""
    Metodo que escucha el socket del servidor y se dedica a imprimir los mensajes parseados que 
    recibe del servidor.
"""

def iniciarPantalla(model, usuario):
    
    pantalla = PantallaPrincipal(model, usuario)
    pantalla.mostrar()
    
    return
    

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
            mensajeError = "Se perdio la conexion con el servidor"
            print(mensajeError)
            vm.onMensajeEntrante(mensajeError)

def getMensajesServidor(mensajeRecibido):
    retorno = []
    mensajes = mensajeRecibido.decode("utf-8").split("\n")
    for m in mensajes:
        mensajesSplit = m.split('|')
        for m2 in mensajesSplit:
            retorno.append(m2)
    return retorno


"""
    Metodo que se dedica a parsear los mensajes que envia el servidor dependiendo de la modalidad de los mismos 
"""
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
            datosJugador = j.replace("{","[").replace("}","]")
            datosJugador = datosJugador.strip('][').split(', ')
            print("dato jugador")
            print(datosJugador)
            print(datosJugador[4])
            if datosJugador[0] == vm.MiNombre:
                vm.MiPuntaje = datosJugador[4]
                vm.MiSaldo = datosJugador[1]
                vm.MiEstado = datosJugador[2]
                if len(datosJugador[3]) > 2:
                    vm.MisCartas = datosJugador[3].strip('][').split(',')
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

def soy(usr):
    comando = "soy " + usr
    sock.send(comando.encode())
    vm.MiNombre = usr.replace('\n','')

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

#Verifico que comando esta queriendo enviar en la consola y lo encapsulo en la funcion correspondiente (que tambien se invoca desde la GUI)
def analizarComandoEnviado(linea):
    try:
        comando = linea.split(" ")[0].replace('\n','')
        if (comando == "mensaje"):
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
        print("error al enviar el comando")

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
    start_new_thread(iniciarPantalla, (vm,""))
    while True:
        newMsg = sys.stdin.readline()
        analizarComandoEnviado(newMsg)
        #sock.send(newMsg.encode())
    sock.close()


if __name__ == "__main__":
    vm.ee.on("pedirCartaEvent", pedirCarta)
    vm.ee.on("plantarseEvent", plantarse)
    vm.ee.on("separarEvent", separar)
    vm.ee.on("fondearEvent", fondear)
    vm.ee.on("apostarEvent", apostar)
    vm.ee.on("doblarEvent", doblar)
    vm.ee.on("enviarMensajeEvent", enviarMensaje)

    inicioCliente()
    #start_new_thread(mostrarInterfaz, (vm,))


