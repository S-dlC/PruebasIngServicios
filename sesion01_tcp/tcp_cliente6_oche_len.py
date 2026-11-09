import socket, sys

def envia_mensaje(sock, texto):
    datos = texto.encode("utf-8")
    cabecera = ("%d\n" % len(datos)).encode("ascii")
    sock.sendall(cabecera + datos)

def recibe_mensaje(f):
    cabecera = f.readline()
    if cabecera == b"":
        return None
    longitud = int(cabecera)
    datos = f.read(longitud)
    if len(datos) < longitud:
        return None
    return datos.decode("utf-8")

servidor, puerto = "localhost", 9999
if len(sys.argv) > 1:
    servidor = sys.argv[1]
if len(sys.argv) > 2:
    puerto = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((servidor, puerto))
f = s.makefile("rb")
for linea in ["UNO", "DOS", "TRES con\nsalto y ñ"]:
    envia_mensaje(s, linea)
for _ in range(3):
    print(repr(recibe_mensaje(f)))
f.close()
s.close()
