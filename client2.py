import socket, select, string, sys
from datetime import datetime
from pip._vendor.distlib.compat import raw_input

# Le damos formato a la respuesta del servidor, incluyendo la hora, cuando se envia un mensaje
def display():
    ahora = datetime.now()
    you = "\33[33m\33[1m" + " [" + str(ahora.hour) + ":" + str(ahora.minute) + "] Tu: " + "\33[0m"
    sys.stdout.write(you)
    sys.stdout.flush()


def main():
    if len(
            sys.argv) < 2:  # Si el cliente se inicializa con argumentos (ip del servidor) se omite el pedido de IP del servidor al cual conectarse.
        host = raw_input("Ingrese ip del servidor: ")
    else:
        host = sys.argv[1]

    port = 5001

    # Preguntamos por el usuario para registrarlo en el servidor como primer paso
    name = raw_input("\33[34m\33[1m CREANDO NUEVO ID:\n Ingrese nombre de usuario:")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(200)

    # Se conecta con el servidor
    try:
        s.connect((host, port))
    except:
        print("\33[31m\33[1m No se pudo conectar al servidor \33[0m")

        sys.exit()

    # si se pudo conectar, sigue por aca
    s.send(bytes(name, 'utf-8'))
    display()
    while 1:
        socket_list = [sys.stdin, s]

        # Obtenemos la lista de socket disponibles
        rList, wList, error_list = select.select(socket_list, [], [])

        for sock in rList:
            # Mensaje entrante del servidor, si no hay datos, se informa la desconexion y se cierra el cliente
            if sock == s:
                data = sock.recv(4096)
                if not data:
                    print('\33[31m\33[1m \rDESCONECTADO!!\n \33[0m')

                    sys.exit()
                else:
                    sys.stdout.write(data)
                    display()

            # El usuario envia un mensaje al servidor
            else:
                msg = sys.stdin.readline()
                s.send(msg)
                display()


if __name__ == "__main__":
    main()