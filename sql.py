import sqlite3

sqlCrearTablaPartida = """
    CREATE TABLE IF NOT EXISTS partidas (
        id integer PRIMARY KEY,
        fecha datetime default timestamp,
        total_jugadores int
    );
"""

sqlCrearTablaJugadores = """
    CREATE TABLE IF NOT EXISTS jugadores (
        id text,
        dinero int,
        primary key(id)
    );
"""

sqlCrearTablaPartidaJugadores = """
    CREATE TABLE IF NOT EXISTS partida_jugadores (
        partida_id,
        jugador_id text,
        estado text,
        primary key (partida_id, jugador_id)
    );
"""

sqlCrearTablaPartidaCartas = """
    CREATE TABLE IF NOT EXISTS partida_cartas (
        id integer PRIMARY KEY,
        partida_id,
        carta text
    );
"""

class ManejadorDB():

    def loguear(self, mensaje):
        print("[ManejadorDB] " + mensaje)

    def __init__(self, reiniciarTablas):
        conexion = sqlite3.connect(r"blackjack.db")
        try:
            sqlCursor = conexion.cursor()
            if reiniciarTablas:
                self.loguear("Droppeando tablas")
                sqlCursor.execute("DROP TABLE partidas")
                sqlCursor.execute("DROP TABLE jugadores")
                sqlCursor.execute("DROP TABLE partida_jugadores")
                sqlCursor.execute("DROP TABLE partida_cartas")
            self.loguear("Creando tabla de partidas")
            sqlCursor.execute(sqlCrearTablaPartida)
            self.loguear("Creando tabla de jugadores")
            sqlCursor.execute(sqlCrearTablaJugadores)
            self.loguear("Creando tabla de partida_jugadores")
            sqlCursor.execute(sqlCrearTablaPartidaJugadores)
            self.loguear("Creando tabla de partida_cartas")
            sqlCursor.execute(sqlCrearTablaPartidaCartas)
        except Exception as e:
            print(e)


    def registrarPartida(self, jugadores):
        self.loguear("Registrando partida")
        conexion = sqlite3.connect(r"blackjack.db")
        sqlCursor = conexion.cursor()
        sqlCursor.execute("INSERT INTO partidas(total_jugadores) VALUES (?)", (len(jugadores),))
        conexion.commit()
        idConexion = sqlCursor.lastrowid
        self.loguear("Partida registrada con ID " + str(idConexion))
        for i in range(len(jugadores)):
            sqlCursor.execute("INSERT INTO partida_jugadores (partida_id, jugador_id, estado) VALUES (?,?,?)", (idConexion, jugadores[i].usuario.nombre, jugadores[i].estadoActual))
            descripciones = jugadores[i].manoActual.obtenerDescripcionCartas()
            for desc in descripciones:
                sqlCursor.execute("INSERT INTO partida_cartas (partida_id, carta) VALUES (?, ?)", (idConexion, desc))
        conexion.commit()
        conexion.close()

    def obtenerEstadisticas(self):
        self.loguear("Obteniendo estadisticas")
        conexion = sqlite3.connect(r"blackjack.db")
        sqlCursor = conexion.cursor()
        sqlCursor.execute("""
            SELECT jugador_id,
            sum(case when estado = 'finalizado_ganador' then 1 else 0 end) ganadas,
            sum(case when estado = 'finalizado_empate' then 1 else 0 end) empatadas,
            sum(case when estado = 'finalizado_perdido' then 1 else 0 end) perdidas
            FROM partida_jugadores
            GROUP BY jugador_id
        """)
        filas = sqlCursor.fetchall()
        sqlCursor.execute("""
            SELECT carta, sum(1)
            FROM partida_cartas
            GROUP BY carta
            ORDER BY sum(1) DESC
        """)
        cartas = sqlCursor.fetchall()
        conexion.close()
        return (filas, cartas)
