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
    longitud = struct.unpack(">H", cabecera)[0]   # unpack devuelve una tupla
    datos = recvall(sock, longitud)
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
    while True:
        mensaje = recibe_mensaje(sd)
        if mensaje is None:
            break
        envia_mensaje(sd, mensaje[::-1])
    sd.close()
