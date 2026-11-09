import socket, sys

def envia_mensaje(sock, texto):
    datos = texto.encode("utf-8")
    cabecera = ("%d\n" % len(datos)).encode("ascii")   # longitud en BYTES
    sock.sendall(cabecera + datos)

def recibe_mensaje(f):
    """f: fichero binario (makefile("rb")). Devuelve str o None si el otro cerró."""
    cabecera = f.readline()
    if cabecera == b"":
        return None
    longitud = int(cabecera)
    datos = f.read(longitud)          # bloquea hasta tener los n bytes (o EOF)
    if len(datos) < longitud:
        return None
    return datos.decode("utf-8")

puerto = 9999
if len(sys.argv) > 1:
    puerto = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", puerto))
s.listen(5)

while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    print("Nuevo cliente conectado desde %s, %d" % origen)
    f = sd.makefile("rb")
    while True:
        mensaje = recibe_mensaje(f)
        if mensaje is None:
            break
        envia_mensaje(sd, mensaje[::-1])
    f.close()
    sd.close()
