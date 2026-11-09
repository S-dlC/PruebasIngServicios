import socket
import sys
import random

puerto = 9999
if len(sys.argv) > 1:
    puerto = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", puerto))
print("Escuchando en el puerto", puerto)

while True:
    datagrama, origen = s.recvfrom(1024)
    if random.randint(0, 1) == 0:
        print("Simulando paquete perdido")
    else:
        texto = datagrama.decode("utf-8")
        print("Datagrama recibido desde", origen)
        print(texto)