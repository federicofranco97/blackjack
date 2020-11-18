import socket
import sys
import json
import codigoMensaje
from pathlib import Path

from pip._vendor.distlib.compat import raw_input
from gui import *
from guiViewModel import GuiViewModel
from pantallautil import PantallaBase
from pantallaingreso import PantallaIngreso
from pantallaprincipal import PantallaPrincipal
from datosMensaje import DatosMensaje

usarGUI = True
diccionario = {}
vm = GuiViewModel()
sock = None

# Iniciamos la GUI
def iniciarPantalla():
    pantallaBase = PantallaBase()
    pantallainicial = PantallaIngreso(vm, pantallaBase.getRoot())
    pantallainicial.mostrar()
    pantallainicial.root.withdraw()
    if vm.Validado:
        print("Entrando a jugar\n")
        pantallaPrincipal = PantallaPrincipal(vm, pantallaBase.getRoot())
        pantallaPrincipal.mostrar()
        pantallaPrincipal.root.withdraw()
    else:
        print("Saliendo del juego\n")
        os._exit(0)
    return

def escucharServidorThread():
    start_new_thread(escucharServidor, ())

# Este metodo corre permanentemente escuchando el socket para recibir los mensajes del servidor
def escucharServidor():
    while 1:
        try:
            data = sock.recv(4096)
            if not data:
                continue
            else:
                #Imprimo los mensajes del servidor
                print(data)
                info = DatosMensaje()
                mensajes = getMensajesServidor(data)
                for m in mensajes:
                    mensajeParseado = parsearMensajeServidor(m, info)
        except socket.timeout:
            mensajeError = diccionario[vm.lenguaje]["conexionPerdida"]
            print(mensajeError)
            vm.onMensajeEntrante(mensajeError, "SERVIDOR")



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
def parsearMensajeServidor(mensajeRecibido, info):
    mensajeBase = mensajeRecibido.split(":")
    comando = mensajeBase[0] if len(mensajeBase) > 0 else mensajeRecibido
    argumentos = mensajeBase[1:] if len(mensajeBase) > 0 else []

    if comando == "comandos":
        formateo = str(argumentos[0]).split("#")
        print("Comandos Posibles: " + " - ".join(formateo))
        vm.onRefreshButtons(formateo)
    elif comando == "mensaje":
        formateo = str(argumentos[0])
        info.Mensaje = formateo
        print(formateo)
    elif comando == "codigo":
        if argumentos[0] == codigoMensaje.ALIAS_ACEPTADO:
            vm.onSoyAceptado()
        elif argumentos[0] == codigoMensaje.ALIAS_RECHAZADO:
            vm.onSoyRechazado(info.Mensaje)
        elif argumentos[0] == codigoMensaje.PARTIDA_FINALIZADA:
            vm.Turno = ""
            vm.onJuegoTerminado()
        elif argumentos[0] == codigoMensaje.PARTIDA_INICIADA:
            vm.onJuegoComenzado(info.Mensaje)
        elif argumentos[0] == codigoMensaje.MENSAJE:
            if info.Mensaje != "":
                vm.onMensajeEntrante(info.Mensaje, "MENSAJE")
        elif argumentos[0] == codigoMensaje.ESTADISTICAS:
            vm.onEstadisticasRecibidas(info.Mensaje)
        else:
            if info.Mensaje != "":
                vm.onMensajeEntrante(info.Mensaje, "SERVIDOR")
    elif comando == "status":
        formateo = str(argumentos).split("#")[1]
        return formateo.replace("\\n", "")
    elif comando == "banca":
        formateo = str(argumentos[0]).split("#")
        cartasBanca = str(formateo[0])
        cartasBanca = cartasBanca.replace("{", "").replace("}", "").split(",")
        vm.onPuntajeBancaChanged(formateo[1], cartasBanca)
    elif comando == "jugadores":
        jugadores = argumentos[0].split("#")
        vm.Jugadores = []
        estadisticas = ""
        for j in jugadores:
            datosJugador = j.replace("{", "[").replace("}", "]")
            datosJugador = datosJugador.strip('][').split(', ')
            if datosJugador[0] == vm.MiNombre:
                vm.MiPuntaje = datosJugador[4]
                vm.MiSaldo = datosJugador[1]
                vm.MiEstado = datosJugador[2]
                if len(datosJugador[3]) > 2:
                    tempCartas = datosJugador[3].strip('][').split(',')
                    if vm.MisCartas != tempCartas:
                        vm.MisCartas = tempCartas
                        print(imprimirMano(tempCartas))
                else:
                    vm.MisCartas = []
                vm.onEstadoChanged(vm.MiEstado)
                if vm.MiEstado == "activo":
                    if vm.Turno != vm.MiNombre:
                        vm.onTurnoChanged(vm.MiNombre)
            else:
                if datosJugador[2] == "activo":
                    vm.onTurnoChanged(datosJugador[0])
                estadisticas += datosJugador[0] + ' $' + datosJugador[1] + ' (' + datosJugador[2] + ')' + '\n'

        vm.onJugadoresRefreshed(estadisticas)
    else:
        return str(argumentos)


# Muestra la mano actual por consola
def imprimirMano(pMano):
    mensaje = str(pMano)
    return diccionario[vm.lenguaje]["tuMano"].replace("{0}", mensaje)


# Wrapper para enviar el comando soy
def soy(usr):
    if usr is None or usr == "":
        vm.onSoyRechazado(diccionario[vm.lenguaje]["nombreVacio"])
        return
    comando = "soy " + usr + " " + vm.lenguaje
    sock.send(comando.encode())
    vm.MiNombre = usr.replace('\n', '')


# Wrapper para enviar el pedido de carta
def pedirCarta():
    print("pedir carta")
    comando = "pedir"
    sock.send(comando.encode())


# Wrapper para solicitar plantarse
def plantarse():
    print("me planto")
    comando = "plantarse"
    sock.send(comando.encode())


# Wrapper para enviar la solicitud de doblar
def doblar():
    print("doblar apuesta")
    comando = "doblar"
    sock.send(comando.encode())


# Wrapper para enviar el fondeo
def fondear(monto):
    print("fondear " + monto)
    comando = "ingresar " + monto
    sock.send(comando.encode())


# Wrapper para enviar la apuesta
def apostar(monto):
    print("apostando " + monto)
    comando = "apostar " + monto
    sock.send(comando.encode())


# Wrapper para enviar un mensaje por el socket
def enviarMensaje(mensaje):
    print("enviando mensaje: " + mensaje)
    comando = "mensaje " + mensaje
    sock.send(comando.encode())

def estadisticas():
    print("pidiendo estadisticas")
    comando = "estadisticas"
    sock.send(comando.encode())


# Se conecta al servidor con los parametros solicitados
def conectar(ip, puerto):
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, int(puerto)))
        vm.onConnected()
    except Exception as e:
        print(diccionario[vm.lenguaje]["errorConexion"] + str(e))
        vm.onConnectError(diccionario[vm.lenguaje]["errorConexion"] + str(e))
        return False
    return True


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
        elif comando == "doblar":
            doblar()
        elif comando == "estadisticas":
            estadisticas()
    except:
        print(diccionario[vm.lenguaje]["errorComando"])


# Metodo que inicializa el cliente, y decide si entrar en modo consola o con GUI
def inicioCliente():
    if not usarGUI:
        while True:
            host = raw_input(diccionario[vm.lenguaje]["solicitarIp"])
            port = raw_input(diccionario[vm.lenguaje]["solicitarPuerto"])
            if conectar(host, port):
                break
        print(diccionario[vm.lenguaje]["mensajeBienvenida"])

    if usarGUI:
        #start_new_thread(escucharServidor, ())
        iniciarPantalla()

    if not usarGUI:
        start_new_thread(escucharServidor, ())
        while True:
            newMsg = sys.stdin.readline()
            analizarComandoEnviado(newMsg)
        sock.close()

    print("Exit")


# Punto de entrada del Cliente
if __name__ == "__main__":
    files = os.listdir("lenguaje")
    for f in files:
        with open(os.path.join("lenguaje", f)) as json_file:
            name = Path(f).resolve().stem
            diccionario[name] = json.load(json_file)

    #Suscripcion a eventos
    vm.ee.on("pedirCartaEvent", pedirCarta)
    vm.ee.on("plantarseEvent", plantarse)
    vm.ee.on("fondearEvent", fondear)
    vm.ee.on("apostarEvent", apostar)
    vm.ee.on("doblarEvent", doblar)
    vm.ee.on("enviarMensajeEvent", enviarMensaje)
    vm.ee.on("requestConnectionEvent", conectar)
    vm.ee.on("soyEvent", soy)
    vm.ee.on("connectedEvent", escucharServidorThread)
    vm.ee.on("solicitarEstadisticasEvent", estadisticas)
    inicioCliente()
