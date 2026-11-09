import socket, sys, time

def recibe_mensaje(sock):
    """Devuelve una línea completa (bytes, con \r\n) leyendo byte a byte.
    Devuelve b"" si el otro extremo cierra la conexión."""
    buffer = []
    while True:
        byte = sock.recv(1)
        if byte == b"":
            return b""     # cierre (se descarta una línea incompleta)
        buffer.append(byte)
        if byte == b"\n" and len(buffer) >= 2 and buffer[-2] == b"\r":
            return b"".join(buffer)

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
    while True:
        mensaje = recibe_mensaje(sd).decode("utf-8")
        if mensaje == "":
            break
        linea = mensaje[:-2][::-1]
        sd.sendall((linea + "\r\n").encode("utf-8"))
    sd.close()
