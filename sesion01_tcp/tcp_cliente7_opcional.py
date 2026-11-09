import socket, sys, struct

def recvall(sock, n):
    partes = []
    restantes = n
    while restantes > 0:
        trozo = sock.recv(restantes)
        if trozo == b"":
            break
        partes.append(trozo)
        restantes -= len(trozo)
    return b"".join(partes)

def envia_mensaje(sock, texto):
    datos = texto.encode("utf-8")
    if len(datos) > 65535:
        raise ValueError("Mensaje demasiado largo para 2 bytes de longitud")
    sock.sendall(struct.pack(">H", len(datos)) + datos)

def recibe_mensaje(sock):
    cabecera = recvall(sock, 2)
    if len(cabecera) < 2:
        return None
    longitud = struct.unpack(">H", cabecera)[0]
    datos = recvall(sock, longitud)
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
for linea in ["UNO", "DOS", "TRES con\nsalto y ñ"]:
    envia_mensaje(s, linea)
for _ in range(3):
    print(repr(recibe_mensaje(s)))
s.close()
