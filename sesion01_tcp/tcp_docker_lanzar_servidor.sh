#!/bin/bash
# Lanza el servidor oche publicando el puerto 9999 del contenedor como 9090 del anfitrión
docker network create pruebas 2>/dev/null
docker rm -f servidor_oche 2>/dev/null
docker run -d --rm -p 9090:9999 --network pruebas --name servidor_oche \
    -v $(pwd):/app python:3.7 python -u /app/tcp_servidor5_oche_readline.py
docker ps
