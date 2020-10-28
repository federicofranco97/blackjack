import os
import random
import select
import socket
import sys

from pip._vendor.distlib.compat import raw_input

hayJugadoresEnEspera = False
hayPartidaEnCurso = True


# Muestra el estado del servidor, si hay partidas en curso y si hay gente en espera
def imprimirEstadoServidor():
    if hayPartidaEnCurso:
        print("Hay una partida en curso actualmente, al finalizar la ronda podra solicitar unirse a la misma")
    if not hayPartidaEnCurso and hayJugadoresEnEspera:
        print("No hay una partida iniciada, pero hay jugadores en la cola, la partida comenzara brevemente.")
    if not hayPartidaEnCurso and not hayJugadoresEnEspera:
        print("No hay una  partida iniciada, y no hay jugadores en cola,"
              " si no se conecta nadie en breve comenzara solo contra la banca")


# Metodo de inicializacion, pide el nombre de usuario y realiza la conexion al sv
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
        print(str(data),":")
        name = raw_input()
        sock.send(name.encode())

    sock.settimeout(200)
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

    # while 1:
    #     socket_list = [socket.socket(), s]
    #     # Obtenemos la lista de socket disponibles
    #     rList, wList, error_list = select.select(socket_list, [], [])
    #     for sock in rList:
    #         # Mensaje entrante del servidor, si no hay datos, se informa la desconexion y se cierra el cliente
    #         if sock == s:
    #             data = sock.recv(4096)
    #             if not data:
    #                 print('No se pudo conectar con el servidor!!')
    #                 sys.exit()
    #             else:
    #                 sys.stdout.write(data)
    #         # El usuario envia un mensaje al servidor
    #         else:
    #             msg = sys.stdin.readline()
    #             s.send(msg)


if __name__ == "__main__":
    inicioCliente()
