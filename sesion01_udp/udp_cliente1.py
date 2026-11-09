from sys import argv
import socket

#Para que no funcione sin dar valores específicos:
# if len(argv) > 1:
#     print("Uso: python udp_cliente1.py host port")
#     exit(1)

host = "localhost" 
port = 9999

if len(argv) > 1:
    host = argv[1]

if len(argv) > 2:
    port = int(argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

linea = ""

while linea != "FIN":
    linea = input("Ingrese un mensaje o 'FIN' para terminar: ")
    s.sendto(linea.encode(), (host, port)) #ya es encode("utf-8") por defecto

s.close()