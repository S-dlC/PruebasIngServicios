import socket, sys, time

puerto = 9999
retardo = 0
if len(sys.argv) > 1:
    puerto = int(sys.argv[1])
if len(sys.argv) > 2:
    retardo = float(sys.argv[2])   # solo para el experimento del retardo

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", puerto))
s.listen(5)

while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    print("Nuevo cliente conectado desde %s, %d" % origen)
    time.sleep(retardo)
    continuar = True
    while continuar:
        datos = sd.recv(5).decode("utf-8")
        if datos == "":
            print("Conexión cerrada de forma inesperada por el cliente")
            sd.close()
            continuar = False
        elif datos == "FINAL":
            print("Recibido mensaje de finalización")
            sd.close()
            continuar = False
        else:
            print("Recibido mensaje: %s" % datos)
