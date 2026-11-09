#!/bin/bash
# Uso: ./udp_docker_lanzar_cliente.sh [broadcast]
BROADCAST=${1:-172.18.255.255}    # cambia el valor por defecto por el tuyo
docker run -it --rm --name cliente --network pruebas \
    -v $(pwd):/app python:3.7 python /app/udp_cliente6_broadcast.py $BROADCAST