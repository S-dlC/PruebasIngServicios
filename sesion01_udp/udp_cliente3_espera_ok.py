import socket
import sys

servidor = "localhost"
puerto = 9999
if len(sys.argv) > 1:
    servidor = sys.argv[1]
if len(sys.argv) > 2:
    puerto = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

numero = 1
while True:
    linea = input("Texto a enviar (FIN para terminar): ")
    if linea == "FIN":
        break
    mensaje = str(numero) + ": " + linea
    s.sendto(mensaje.encode("utf-8"), (servidor, puerto))
    numero += 1

    s.settimeout(0.1)
    try:
        respuesta, origen = s.recvfrom(1024)
        respuesta = respuesta.decode("utf-8")
        if respuesta == "OK":
            print("Recibida confirmación")
        else:
            print("Recibido datagrama no esperado")
    except socket.timeout:
        print("ERROR. El datagrama de confirmación no llega")

s.close()