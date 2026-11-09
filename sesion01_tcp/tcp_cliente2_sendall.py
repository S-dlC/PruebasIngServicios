import socket, sys

servidor, puerto, bloque = "localhost", 9999, "ABCDE"
if len(sys.argv) > 1:
    servidor = sys.argv[1]
if len(sys.argv) > 2:
    puerto = int(sys.argv[2])
if len(sys.argv) > 3:
    bloque = sys.argv[3]   # para el experimento con "ABCD"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((servidor, puerto))
for _ in range(5):
    s.sendall(bloque.encode("utf-8"))
s.sendall("FINAL".encode("utf-8"))
s.close()
