import socket, sys

def recibe_mensaje(sock):
    buffer = []
    while True:
        byte = sock.recv(1)
        if byte == b"":
            return b""
        buffer.append(byte)
        if byte == b"\n" and len(buffer) >= 2 and buffer[-2] == b"\r":
            return b"".join(buffer)

servidor, puerto = "localhost", 9999
if len(sys.argv) > 1:
    servidor = sys.argv[1]
if len(sys.argv) > 2:
    puerto = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((servidor, puerto))
for linea in ["UNO", "DOS", "TRES"]:
    s.sendall((linea + "\r\n").encode("utf-8"))
for _ in range(3):
    respuesta = recibe_mensaje(s).decode("utf-8")
    print(repr(respuesta))
s.close()
