import os
import random
import select
import socket
import sys
from _thread import *
import threading

from pip._vendor.distlib.compat import raw_input

hayJugadoresEnEspera = False
hayPartidaEnCurso = True


def escucharServidor(sock):
    while 1:
        try:
            data = sock.recv(4096)
            if not data:
                continue
            else:
                # Imprimo los msjs del servidor
                print(str(data))
        except socket.timeout:
            print("Se perdio la conexion con el servidor")


# Muestra el estado del servidor, si hay partidas en curso y si hay gente en espera
def imprimirEstadoServidor():
    if hayPartidaEnCurso:
        print("Hay una partida en curso actualmente, al finalizar la ronda podra solicitar unirse a la misma")
    if not hayPartidaEnCurso and hayJugadoresEnEspera:
        print("No hay una partida iniciada, pero hay jugadores en la cola, la partida comenzara brevemente.")
    if not hayPartidaEnCurso and not hayJugadoresEnEspera:
        print("No hay una  partida iniciada, y no hay jugadores en cola,"
              " si no se conecta nadie en breve comenzara solo contra la banca")


"""
    Metodo que inicializa el cliente, solicita los datos principales como ip del servidor,
    puerto, y luego de realizar la conexion pide el nombre de usuario
"""


def inicioCliente():
    print("Bienvenido al servidor de BlackJack")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(200)
    # Se conecta con el servidor
    # host = '192.168.100.233'
    # port = 3039
    host = raw_input("Por favor ingresa la IP del servidor: ")
    port = raw_input("Por favor ingresa el puerto del servidor: ")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, int(port)))
    except Exception as e:
        print("Ocurrio un error al conectarse con el servidor:", e)
        return
    print("Conectado, bienvenido al servidor!")

    # name = raw_input("Por favor ingrese su nombre: ")
    # si se pudo conectar, envio el nombre del jugador
    # s.send(bytes(name, 'utf-8'))
    # imprimirEstadoServidor()
    data = sock.recv(4096)
    if not data:
        print('Ocurrio un error de conexion con el servidor!!')
        sys.exit()
    else:
        # Primera respuesta del servidor (Ingresa tu nombre)
        print(str(data), ":")
        name = raw_input()
        sock.send(name.encode())

    start_new_thread(escucharServidor(sock))
    while 1:
        newMsg = sys.stdin.readline()
        s.send(newMsg.encode())


if __name__ == "__main__":
    inicioCliente()
