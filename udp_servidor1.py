from sys import argv
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if len(argv) < 1:
    print("Uso: python udp_cliente1.py host port")
    exit(1)

s.bind(("", 9999))


while True:
        datagrama, origen = s.recvfrom(1024)
        print("Se ha recibido: " + str(datagrama.decode()) + "\nDirección: " + str(origen))
    