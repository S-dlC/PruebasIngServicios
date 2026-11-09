import socket, sys, time

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
        mensaje = sd.recv(80).decode("utf-8")
        if mensaje == "":              # el cliente cerró la conexión
            break
        linea = mensaje[:-2][::-1]     # quitar \r\n y dar la vuelta
        sd.sendall((linea + "\r\n").encode("utf-8"))
    sd.close()
