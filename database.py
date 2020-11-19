import pyodbc
import json

from jugador import Jugador
from partida import Partida

connection_string = ""

#Inicializar String de conexion a la BD
def inicializarConnection(servidor, database):
    global connection_string
    connection_string = 'Driver={SQL Server};Server=' + servidor + ';Database=' + database + ';Trusted_Connection=yes;'
    try:
        conn = pyodbc.connect(connection_string)
    except pyodbc.Error as error:
        raise Exception("Error en la conexion: " + error.args[1])

#Esta funcion busca, si la hay, una partida que haya quedado pendiente, solo trae la ultima.
def buscarPartidaPendiente():
    if connection_string == "":
        raise Exception("Inicializar Connection String")
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("Select top 1 * From Partidas Where FechaFinalizacion Is Null Order by 1 Desc")
    dbPartida = cursor.fetchone()
    if dbPartida == None:
        return None

    partida = Partida()
    partida.idPartida = dbPartida[0]
    if dbPartida[3] != "" and dbPartida[3] != None:
        partida.cartas = json.loads(dbPartida[3])

    if dbPartida[4] != "" and dbPartida[4] != None:
        partida.manoBanca = json.loads(dbPartida[4])

    #Busco los jugadores y las manos
    #cursor2 = conn.cursor()
    cursor.execute("exec ObtenerDetallePartida ?", str(partida.idPartida))

    for row in cursor:
        if row[3] in partida.jugadores:
            jugador = partida.jugadores[row[3]]
        else:
            jugador = Jugador(None)
            #jugador.usuario.nombre = row[3]
            jugador.apuestaInicial = row[2]


    return partida

#Esta funcion se utiliza para marcar la finalizacion de la partida
#ganador: B:Banca, J:Jugadores, Nro:IdJugadorMano
def finalizarPartida(idPartida, ganador):
    if connection_string == "":
        raise Exception("Inicializar Connection String")
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute('exec FinalizarPartida ?, ''?'' ', (str(idPartida), ganador))
    cursor.commit()


#Funcion para agregar el uso de una carta (se saca del mazo) en una partida
def agregarCartaUsada(idpartida, carta):
    if connection_string == "":
        raise Exception("Inicializar Connection String")
    cartausada = json.dumps(carta)
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("Select CartasUsadas From Partidas Where IdPartida = " + str(idpartida))
    cartasdb = cursor.fetchone()[0]
    #print(cartasdb)
    #print(type(cartasdb))
    cartas = []
    if cartasdb != "":
        cartas = json.loads(cartasdb)
        cartas.append(carta)
    else:
        cartas.append(cartausada)


    cursor.execute("Update Partidas Set CartasUsadas='" + json.dumps(cartas) + "' where IdPartida=" + str(idpartida))
    conn.commit()

#Se llama para generar una partida en la Base de Datos, devuelve el Id AutoGenerado
def crearPartida():
    if connection_string == "":
        raise Exception("Inicializar Connection String")
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("Insert Into Partidas Select GetDate(),null,''")
    conn.commit()
    cursor.execute("Select @@Identity")
    idpartida = cursor.fetchone()[0]
    return idpartida

#Crea un jugador en la Base de Datos
def crearJugador(alias, dinero):
    if connection_string == "":
        raise Exception("Inicializar Connection String")
    idJugador = buscarJugador(alias)
    if idJugador != 0:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("Update Jugadores Set Dinero += '" + str(dinero) + "' where IdJugador = " + str(idJugador))
        cursor.commit()
        return idJugador

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("Insert Into Jugadores Values ('" + alias + "'," + str(dinero) + ")")
    conn.commit()
    cursor.execute("Select @@Identity")
    idJugador = cursor.fetchone()[0]
    return idJugador

#Busca un jugador por su alias
def buscarJugador(alias):
    if connection_string == "":
        raise Exception("Inicializar Connection String")
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("Select IdJugador From Jugadores where Alias='" + alias + "'")
    rowJugador = cursor.fetchone()
    if rowJugador == None:
        return 0
    return rowJugador[0]

def separarMano(alias, idPartida, mano1, mano2):
    if connection_string == "":
        raise Exception("Inicializar Connection String")
    idJugador = buscarJugador(alias)
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute('exec SplitMano ?, ?, ''?'', ''?'' ', (str(idJugador), str(idPartida), mano1, mano2))
    cursor.commit()

#Funcion para recuperar los Jugadores de una partida
def getjugadores():
    if connection_string == "":
        raise Exception("Inicializar Connection String")
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("Select * from Jugadores")
    for row in cursor:
        print(row)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    inicializarConnection("localhost\\sql2019", "POKER")
    #partida = buscarPartidaPendiente()
    #print(partida)
    crearJugador("player",100)
    #finalizarPartida(9, 'B')

    ##id = crearPartida()
    carta = {
        "palo": "C",
        "numero": "A"
    }
    #agregarCartaUsada(9, carta)
    #getjugadores()
