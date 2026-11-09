import socket
import sys
import secrets
import time

servidor = "localhost"
puerto = 9999
if len(sys.argv) > 1:
    servidor = sys.argv[1]
if len(sys.argv) > 2:
    puerto = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((servidor, puerto))

while True:
    linea = input("Texto a enviar (FIN para terminar): ")
    if linea == "FIN":
        break
    id_datagrama = secrets.token_hex(4)
    datos = (id_datagrama + ": " + linea).encode("utf-8")
    esperado = "OK " + id_datagrama

    timeout = 0.1
    confirmado = False
    while timeout <= 2 and not confirmado:
        s.send(datos)
        s.settimeout(timeout)
        try:
            while True:
                respuesta = s.recv(1024).decode("utf-8")
                if respuesta == esperado:
                    print("Recibida confirmación", respuesta)
                    confirmado = True
                    break
                print("Ignorada confirmación de otro datagrama:", respuesta)
        except socket.timeout:
            print("Timeout de", timeout, "s sin confirmación, reintentando")
            timeout *= 2
        except ConnectionRefusedError:
            print("Puerto inaccesible, reintentando")
            time.sleep(timeout)
            timeout *= 2

    if not confirmado:
        print("Puede que el servidor esté caído. Inténtelo más tarde")
        break

s.close()