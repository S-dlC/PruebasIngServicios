import socket
import sys
import random

puerto = 9999
if len(sys.argv) > 1:
    puerto = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", puerto))
print("Escuchando en el puerto", puerto)

recibidos = set()

while True:
    datagrama, origen = s.recvfrom(1024)
    if random.randint(0, 1) == 0:
        print("Simulando paquete perdido")
        continue

    id_datagrama, texto = datagrama.decode("utf-8").split(": ", 1)
    if id_datagrama in recibidos:
        print("Duplicado", id_datagrama, "- solo reenvío la confirmación")
    else:
        recibidos.add(id_datagrama)
        print("Datagrama recibido desde", origen)
        print(texto)   # aquí iría la acción real asociada al datagrama
    s.sendto(("OK " + id_datagrama).encode("utf-8"), origen)