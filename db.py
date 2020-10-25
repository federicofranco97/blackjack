import sys
import pyodbc
import json

from jugador import Jugador

connection_string = ""

#Inicializar String de conexion a la BD
def inicializarConnection(servidor, database):
    global connection_string
    connection_string = 'Driver={SQL Server};Server=' + servidor + ';Database=' + database + ';Trusted_Connection=yes;'
    try:
        conn = pyodbc.connect(connection_string)
    except pyodbc.Error as error:
        raise Exception("Error en la conexion: " + error.args[1])


#Funcion para agregar el uso de una carta (se saca del mazo) en una partida
def agregarCartaUsada(idpartida, carta):
    if connection_string == "":
        raise Exception("Inicializar Connection String")
    cartausada = json.dumps(carta)
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("Select CartasUsadas From Partidas Where IdPartida = " + str(idpartida))
    cartasdb = cursor.fetchone()[0]
    print(cartasdb)
    print(type(cartasdb))
    cartas = []
    if cartasdb != "":
        cartas = json.loads(cartasdb)
        cartas.append(carta)
    else:
        cartas.append(cartausada)


    cursor.execute("Update Partidas Set CartasUsadas='" + json.dumps(cartas) + "' where IdPartida=" + str(idpartida))
    conn.commit()

    #print(cartas)

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
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("Insert Into Jugadores Values ('" + alias + "'," + dinero + ")")
    conn.commit()

#Busca un jugador por su alias
def buscarJugador(alias):
    if connection_string == "":
        raise Exception("Inicializar Connection String")
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("Select * From Jugadores where Alias='" + alias + "'")
    rowJugador = cursor.fetchone()
    jugador = Jugador(rowJugador["IdJugador"], rowJugador["Alias"], rowJugador["Dinero"])
    return jugador

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
    ##id = crearPartida()
    carta = {
        "palo": "C",
        "numero": "A"
    }
    #agregarCartaUsada(9, carta)
    getjugadores()
