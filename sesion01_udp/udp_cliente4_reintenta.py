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
    datos = (str(numero) + ": " + linea).encode("utf-8")

    timeout = 0.1
    confirmado = False
    while timeout <= 2:
        s.sendto(datos, (servidor, puerto))
        s.settimeout(timeout)
        try:
            respuesta, origen = s.recvfrom(1024)
            if respuesta.decode("utf-8") == "OK":
                print("Recibida confirmación")
                confirmado = True
                break
            else:
                print("Recibido datagrama no esperado")
        except socket.timeout:
            print("Timeout de", timeout, "s sin confirmación, reintentando")
        timeout *= 2

    if not confirmado:
        print("Puede que el servidor esté caído. Inténtelo más tarde")
        break
    numero += 1

s.close()