import socket, sys

servidor, puerto = "localhost", 9999
if len(sys.argv) > 1:
    servidor = sys.argv[1]
if len(sys.argv) > 2:
    puerto = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((servidor, puerto))
for linea in ["HOLA", "Esto es una prueba", "UNO"]:
    s.sendall((linea + "\r\n").encode("utf-8"))
    respuesta = s.recv(80).decode("utf-8")   # intercalado: envía y lee
    print(repr(respuesta))
s.close()
