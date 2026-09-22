from sys import argv
import socket

if len(argv) < 1:
    print("Uso: python udp_cliente1.py host port")
    exit(1)
#igual falta añadir selección de ports
host = argv[1]
port = int(argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
linea = ""

while linea != "FIN":
    linea = input("Ingrese un mensaje o 'FIN' para terminar")
    s.sendto(linea.encode(), (host, port))

