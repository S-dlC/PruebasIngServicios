import socket
import sys

broadcast = "255.255.255.255"
if len(sys.argv) > 1:
    broadcast = sys.argv[1]
PUERTO = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

s.sendto("BUSCANDO HOLA".encode("utf-8"), (broadcast, PUERTO))

s.settimeout(2)
primero = None
try:
    while True:
        datagrama, origen = s.recvfrom(1024)
        print("Responde el servidor", origen[0], ":", datagrama.decode("utf-8"))
        if primero is None:
            primero = origen[0]
except socket.timeout:
    pass

if primero is None:
    print("No ha respondido ningún servidor")
else:
    s.sendto("HOLA".encode("utf-8"), (primero, PUERTO))
    try:
        datagrama, origen = s.recvfrom(1024)
        print("Respuesta del servicio:", datagrama.decode("utf-8"))
    except socket.timeout:
        print("El servidor no respondió al HOLA")

s.close()