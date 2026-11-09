import socket, sys, time

def recvall(sock, n):
    """Lee exactamente n bytes (o menos si el otro extremo cierra antes)."""
    partes = []
    restantes = n
    while restantes > 0:
        trozo = sock.recv(restantes)   # pide solo lo que falta
        if trozo == b"":               # el otro extremo cerró: no llegarán más
            break
        partes.append(trozo)
        restantes -= len(trozo)
    return b"".join(partes)

puerto = 9999
retardo = 0
if len(sys.argv) > 1:
    puerto = int(sys.argv[1])
if len(sys.argv) > 2:
    retardo = float(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", puerto))
s.listen(5)

while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    print("Nuevo cliente conectado desde %s, %d" % origen)
    time.sleep(retardo)
    continuar = True
    while continuar:
        datos = recvall(sd, 5).decode("utf-8")
        if datos == "":
            print("Conexión cerrada de forma inesperada por el cliente")
            sd.close()
            continuar = False
        elif datos == "FINAL":
            print("Recibido mensaje de finalización")
            sd.close()
            continuar = False
        else:
            print("Recibido mensaje: %s" % datos)
