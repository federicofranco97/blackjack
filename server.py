import socket

users = {"fede": "test", "fede2": "test2"}

HOST = '192.168.100.7'
PORT = 9999
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(10)
print("Listening")
s = server_socket.accept()
print("Connected")


def login(username, password):
    if username in users:
        if users[username] == password:
            print("Login Exitoso")
        else:
            print("Credenciales erroneas")
    else:
        print("Usuario no encontrado")


