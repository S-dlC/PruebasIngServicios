import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(("", 12345))
print("Escuchando en el puerto 12345")

while True:
    datagrama, origen = s.recvfrom(1024)
    texto = datagrama.decode("utf-8")
    print("Recibido", texto, "desde", origen)
    if texto == "BUSCANDO HOLA":
        s.sendto("IMPLEMENTO HOLA".encode("utf-8"), origen)
    elif texto == "HOLA":
        s.sendto(("HOLA: " + origen[0]).encode("utf-8"), origen)