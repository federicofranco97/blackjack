import os
import random
import select
import socket
import sys
from _thread import *
import logging
import re

from pip._vendor.distlib.compat import raw_input

hayJugadoresEnEspera = False
hayPartidaEnCurso = True

"""
    Metodo que escucha el socket del servidor y se dedica a imprimir los mensajes parseados que 
    recibe del servidor.
"""


def escucharServidor(sock):
    while 1:
        try:
            data = sock.recv(4096)
            if not data:
                continue
            else:
                # Imprimo los msjs del servidor
                print(parsearMensajesServidor(data))
        except socket.timeout:
            print("Se perdio la conexion con el servidor")


"""
    Metodo que se dedica a parsear los mensajes que envia el servidor dependiendo de la modalidiad
    de los mismos 
"""


def parsearMensajesServidor(mensajeRecibido):
    mensajeBase = mensajeRecibido.decode("utf-8").split("|")
    comando = mensajeBase[0] if len(mensajeBase) > 0 else mensajeRecibido
    argumentos = mensajeBase[1:] if len(mensajeBase) > 0 else []
    if comando == "mensaje":
        test = str(argumentos).split("'")[1]
        test = test.replace("\\n","")
        # for i in test:
        #     if i == "\n":
        #         test.remove(i)
        return test
    else:
        return str(argumentos)




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
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, int(port)))
    except Exception as e:
        print("Ocurrio un error al conectarse con el servidor:", e)
        return
    print("Conectado, bienvenido al servidor!")

    print("Separo el thread")
    start_new_thread(escucharServidor, (sock,))
    while True:
        newMsg = sys.stdin.readline()
        sock.send(newMsg.encode())
    sock.close()


if __name__ == "__main__":
    inicioCliente()
