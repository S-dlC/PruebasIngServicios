from sys import argv
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

puerto = 9999

if len(argv) > 1:
    puerto = int(argv[1])

s.bind(("", puerto))
print("Escuchando en el puerto: ", puerto)

while True:
        datagrama, origen = s.recvfrom(1024)
        print("Se ha recibido: " + str(datagrama.decode("utf-8")) + "\nDirección: " + str(origen))
    