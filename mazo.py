import random

"""
    Clase que representa una colección de barajas, o sea que, al mismo tiempo, representa una colección de cartas.
    A través de esta clase se mezclan los mazos, y se extraen las cartas de la pila. En el caso que nos quedemos sin cartas,
    se procedera a mezclar las descartadas.
"""
class Mazo():

    def __init__(self):
        self.cartas = []

    def _generarCartas(self):
        mix = []
        for z in range(4):
            for x in range(13):
                for y in range(4):
                    val = x+1
                    val = 14 if val == 1 else val
                    mix.append(Carta(val, y+1))
        random.shuffle(mix)
        return mix.copy()

    def mezclar(self):
        self.cartas = self._generarCartas()

    def proximaCarta(self):
        if len(self.cartas) == 0:
            self.cartas = self._generarCartas()
        return self.cartas.pop()

"""
    Clase que representa a una carta. Tiene la propiedad de ser visible o no (la segunda carta del croupier no se muestra hsata que el resto haya jugado).
    Ademas tiene valor y palo, para poder representar luego las cartas.
"""
class Carta():

    def __init__(self, valor, palo, visible = True):
        self.valor = valor
        self.palo = palo
        self.visible = visible

    def mostrar(self):
        self.visible = True

    def ocultar(self):
        self.visible = False

"""
    Clase que representa una mano
"""
class Mano():

    def __init__(self, pDiccionario):
        self.apuesta = 0
        self.estado = "sin_apuesta"
        self.cartas = []
        self.diccionario = pDiccionario

        self.valores = {
            14: "As",
            2: "Dos",
            3: "Tres",
            4: "Cuatro",
            5: "Cinco",
            6: "Seis",
            7: "Siete",
            8: "Ocho",
            9: "Nueve",
            10: "Diez",
            11: "Jack",
            12: "Reina",
            13: "Rey"
        }

        self.palos = {
            1: "corazones",
            2: "picas",
            3: "diamantes",
            4: "treboles"
        }

    def agregarApuesta(self, monto):
        self.apuesta += monto

    def obtenerValores(self):
        valores = []
        for carta in self.cartas:
            if carta.visible == True:
                valores.append(str(carta.palo) + "-" + str(carta.valor))
        return valores

    def agregarCarta(self, carta):
        self.cartas.append(carta)

    def obtenerDescripcionCompleta(self, idioma):
        return self.diccionario[idioma]["compuestoPor"].replace("{0}", str(self.obtenerPuntaje())).replace("{1}", str(self.obtenerDescripcion(idioma)))
        #return str(self.obtenerPuntaje()) + " compuestos por " + str(self.obtenerDescripcion())

    def obtenerDescripcionCartas(self, idioma):
        descripciones = []
        for carta in self.cartas:
            nombre = self.valores[carta.valor]
            nombre = self.diccionario[idioma][nombre]
            palo = self.palos[carta.palo]
            palo = self.diccionario[idioma][palo]
            #nombreFinal = nombre + " de " + palo
            nombreFinal = self.diccionario[idioma]["descripcionCarta"].replace("{0}", nombre).replace("{1}", palo)
            descripciones.append(nombreFinal)
        return descripciones

    def obtenerDescripcion(self, idioma):
        descripciones = []
        for carta in self.cartas:
            if carta.visible == True:
                nombre = self.valores[carta.valor]
                nombre = self.diccionario[idioma][nombre]
                palo = self.palos[carta.palo]
                palo = self.diccionario[idioma][palo]
                #nombreFinal = nombre + " de " + palo
                nombreFinal = self.diccionario[idioma]["descripcionCarta"].replace("{0}", nombre).replace("{1}", palo)
                descripciones.append(nombreFinal)
            else:
                descripciones.append(self.diccionario[idioma]["cartaBocaAbajo"])
        return ', '.join(descripciones)

    def mostrarTodas(self):
        for carta in range(len(self.cartas)):
            self.cartas[carta].visible = True

    def obtenerPuntaje(self):
        total = 0
        for carta in self.cartas:
            if carta.visible == True:
                valor = carta.valor
                if valor == 11 or valor == 12 or valor == 13:
                    total += 10
                elif valor == 14:
                    if total >= 11: total += 1
                    if total < 11: total += 11
                else:
                    total += valor
        return total