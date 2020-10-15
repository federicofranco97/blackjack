# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import random
import socket

from pip._vendor.distlib.compat import raw_input

# Mazo de cartas
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4
# cantidad de plata para apostar
availableMoney = 1000


# Reparte 2 cartas al jugador
def deal(deck):
    hand = []
    for i in range(2):
        random.shuffle(deck)
        card = deck.pop()
        if card == 11: card = "J"
        if card == 12: card = "Q"
        if card == 13: card = "K"
        if card == 14: card = "A"
        hand.append(card)
    return hand


# Vuelve a comenzar el juego
def play_again():
    again = raw_input("¿Quieres volver a jugar? (Y/N) : ").lower()
    if again == "y":
        dealer_hand = []
        player_hand = []
        deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4
        game()
    else:
        print
        "Bye!"
        exit()


# Devuelve el total de puntos que acumula la mano
def total(hand):
    total = 0
    for card in hand:
        if card == "J" or card == "Q" or card == "K":
            total += 10
        elif card == "A":
            if total >= 11: total += 1
            if total < 11: total += 11
        else:
            total += card
    return total

def fillDeck():
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4
    random.shuffle(deck)

# SOlicita una carta
def hit(hand):
    
    if len(deck) == 0:
        fillDeck()

    card = deck.pop()
    if card == 11: card = "J"
    if card == 12: card = "Q"
    if card == 13: card = "K"
    if card == 14: card = "A"
    hand.append(card)
    return hand


# Limpia la consola
def clear():
    if os.name == 'nt':
        os.system('CLS')
    if os.name == 'posix':
        os.system('clear')


# Imprime los resultados de la mano
def print_results(dealer_hand, player_hand):
    clear()
    print("La banca tiene " + str(dealer_hand) + " y un total de puntos de " + str(total(dealer_hand)))
    print("Tu mano es " + str(player_hand) + " y sumas un total de puntos de  " + str(total(player_hand)))


# Verifica si el jugador o el dealer tienen blackjack
def blackjack(dealer_hand, player_hand):
    if total(player_hand) == 21:
        print_results(dealer_hand, player_hand)
        print("Felicitaciones! Conseguiste Blackjack!\n")
        play_again()
    elif total(dealer_hand) == 21:
        print_results(dealer_hand, player_hand)
        print("Lo sentimos, perdiste. La banca obtuvo BlackJack.\n")
        play_again()


# Imprime el resultado de la partida para el jugador
def score(dealer_hand, player_hand):
    if total(player_hand) == 21:
        print_results(dealer_hand, player_hand)
        print("Felicitaciones! Obtuviste Blackjack!\n")
    elif total(dealer_hand) == 21:
        print_results(dealer_hand, player_hand)
        print("Lo sientimos, perdiste! La banca tuvo blackjack.\n")
    elif total(player_hand) > 21:
        print_results(dealer_hand, player_hand)
        print("Lo sentimos. Has superado el limite. Perdiste.\n")
    elif total(dealer_hand) > 21:
        print_results(dealer_hand, player_hand)
        print("La banca supero el limite! Ganaste!\n")
    elif total(player_hand) < total(dealer_hand):
        print_results(dealer_hand, player_hand)
        print("Lo Sentimos. El puntaje de la banca es mayor al tuyo. Perdiste!\n")
    elif total(player_hand) > total(dealer_hand):
        print_results(dealer_hand, player_hand)
        print("Felicitaciones! Tu puntaje es mayor al de la banca! Ganaste!\n")


# Pide el ingreso de la cantidad de plata a apostar
def getbet(currentBet):
    bet = raw_input("Cuanto quiere aumentar su apuesta de  " + str(currentBet) + ": ")
    try:
        int(bet)
    except ValueError:
        clear()
        print("Por favor ingrese un numero valido")
        getbet(currentBet)
    else:
        if int(bet) < 0:
            clear()
            print("Por favor ingrese un numero valido")
            getbet(currentBet)
        elif int(bet) > availableMoney:
            clear()
            print("Su apuesta excede el limite que tiene disponible!")
            getbet(currentBet)
        else:
            return int(bet)


# Pide la cantidad de jugadores que van a participar
def countplayers():
    playerstemp = raw_input("Cuantos jugadores hay?")
    try:
        int(playerstemp)
    except ValueError:
        clear()
        print("Por favor ingrese un numero valido")
        countplayers()
    else:
        if int(playerstemp) <= 0:
            clear()
            print("Por favor ingrese un numero valido")
            countplayers()
        else:
            return int(playerstemp)


# Funcion principal que maneja el ciclo del juego
def game():
    choice = 0
    clear()
    print("BIENVENIDO A BLACKJACK!\n")
    # print(countplayers())
    # Inicia la apuesta inicial en 10 y asigno esa como la apuesta del jugador
    # Despues la apuesta minima va a venir del sv
    minimalBet = 10
    bet = minimalBet
    # Reparte la mano del Dealer (Se va a mover al sv)
    dealer_hand = deal(deck)
    # Reparte la mano del jugador
    player_hand = deal(deck)
    while choice != "q":
        print("El dealer tiene " + str(dealer_hand[0]))
        print("Tu mano es " + str(player_hand) + " y suma en total " + str(total(player_hand)))
        print("Tu apuesta es de "+str(bet))
        blackjack(dealer_hand, player_hand)
        choice = raw_input("Elegi la siguiente accion [H]it, [S]tand, [R]aise or [Q]uit: ").lower()
        clear()
        if choice == "h":
            hit(player_hand)
            while total(dealer_hand) < 17:
                hit(dealer_hand)
            score(dealer_hand, player_hand)
            play_again()
        elif choice == "s":
            while total(dealer_hand) < 17:
                hit(dealer_hand)
            score(dealer_hand, player_hand)
            play_again()
        elif choice == "q":
            print("Adios!")
            exit()
        elif choice == "r":
            bet += getbet(bet)
        else:
            print("Adios!")
            exit()


def login():
    username = raw_input("Por favor ingrese su nombre de usuario: ").lower()


def connect():
    host = '192.168.100.233'
    port = 9999
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except Exception as e:
        print("Cannot connect to the server:", e)
    print("Connected")


if __name__ == "__main__":
    game()


