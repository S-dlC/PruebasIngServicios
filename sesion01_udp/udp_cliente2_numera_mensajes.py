import socket
from sys import argv
host = "localhost" 
port = 9999

if len(argv) > 1:
    host = argv[1]

if len(argv) > 2:
    port = int(argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

numero = 1
while True:
    linea = input("Texto a enviar (FIN para terminar): ")
    if linea == "FIN":
        break
    mensaje = str(numero) + ": " + linea
    s.sendto(mensaje.encode("utf-8"), (host, port))
    numero += 1

s.close()