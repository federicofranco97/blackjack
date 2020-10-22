import os
import random
import socket

from pip._vendor.distlib.compat import raw_input


# Metodo para conectarse con el servidor
def conectar():
    # host = '192.168.100.233'
    #port = 9999
    host = raw_input("Por favor ingresa la IP del servidor: ")
    port = raw_input("Por favor ingresa el puerto del servidor: ")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except Exception as e:
        print("Ocurrio un error al conectarse con el servidor:", e)
    print("Conectado, bienvenido al servidor!")


#Consulta el estado del servidor (en partida/esperando jugadores)
def consultarEstado():
        




if __name__ == "__main__":
    conectar()