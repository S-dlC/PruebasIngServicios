#!/bin/bash
docker network create pruebas 2>/dev/null
for i in 1 2 3; do
    docker rm -f servidor$i 2>/dev/null
    docker run -d --name servidor$i --network pruebas \
        -v $(pwd):/app python:3.7 python -u /app/udp_servidor6_broadcast.py
done
docker ps