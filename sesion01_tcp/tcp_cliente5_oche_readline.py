import socket, sys

servidor, puerto = "localhost", 9999
if len(sys.argv) > 1:
    servidor = sys.argv[1]
if len(sys.argv) > 2:
    puerto = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((servidor, puerto))
f = s.makefile(encoding="utf-8", newline="\r\n")
for linea in ["UNO", "DOS", "TRES"]:
    s.sendall((linea + "\r\n").encode("utf-8"))
for _ in range(3):
    print(repr(f.readline()))
f.close()
s.close()
