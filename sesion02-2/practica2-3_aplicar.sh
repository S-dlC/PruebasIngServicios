#!/bin/bash
# Práctica 2.3 (parte Amigos): añade /health y /metrics, reconstruye la imagen amigos:3.0 y relanza contenedores.
# Uso: cd sesion02-2 && bash practica2-3_aplicar.sh      (la carpeta debe contener amigos/ y los lanza-*.sh)
set -e
[ -d amigos/app ] || { echo "Ejecútalo desde la carpeta sesion02-2 (donde está amigos/)"; exit 1; }

# 1. Dependencia en el entorno de desarrollo
source ~/flaskenv/bin/activate && pip install -q prometheus-client

cd amigos
mkdir -p app/health app/metrics

# 2. Blueprint health
cat > app/health/__init__.py <<'EOF'
from flask import Blueprint

health = Blueprint("health", __name__)

from . import views
EOF
cat > app/health/views.py <<'EOF'
from .. import db
from . import health


@health.route("/health")
def health_check():
    try:
        db.session.execute(db.text("SELECT 1"))
        return {"status": "ok", "database": "ok"}, 200
    except Exception:
        return {"status": "error", "database": "error"}, 503
EOF

# 3. Blueprint metrics (versión final del apartado 7.5)
cat > app/metrics/__init__.py <<'EOF'
from flask import Blueprint

metrics = Blueprint("metrics", __name__)

from app.metrics import views
EOF
cat > app/metrics/views.py <<'EOF'
import time
from flask import Response, g
from app.metrics import metrics
from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST
)

http_requests_total = Counter(
    "amigos_http_requests_total",
    "Número total de peticiones HTTP recibidas por Amigos"
)

http_errors_total = Counter(
    "amigos_http_errors_total",
    "Número total de respuestas HTTP de error"
)

http_request_duration_seconds = Histogram(
    "amigos_http_request_duration_seconds",
    "Tiempo de respuesta de las peticiones HTTP en segundos"
)

@metrics.before_app_request
def before_request():
    g.start_time = time.perf_counter()

@metrics.after_app_request
def after_request(response):
    http_requests_total.inc()
    if response.status_code >= 400:
        http_errors_total.inc()
    duration = time.perf_counter() - g.start_time
    http_request_duration_seconds.observe(duration)
    return response

@metrics.route("/metrics")
def metrics_endpoint():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )
EOF

# 4. Registrar los blueprints en create_app (antes de "return app"; idempotente)
python3 - <<'EOF'
p = "app/__init__.py"
s = open(p).read()
if "health_blueprint" not in s:
    add = ("    from .health import health as health_blueprint\n"
           "    app.register_blueprint(health_blueprint)\n\n"
           "    from .metrics import metrics as metrics_blueprint\n"
           "    app.register_blueprint(metrics_blueprint)\n\n")
    assert "    return app" in s, "No encuentro 'return app' en app/__init__.py"
    s = s.replace("    return app", add + "    return app")
    open(p, "w").write(s)
EOF

# 5. Dockerfile con prometheus-client; Dockerfile1w con un solo worker; imagen amigos:3.0 desde Dockerfile1w
grep -q prometheus-client Dockerfile || sed -i 's/^\(RUN pip install flask-sqlalchemy.*\)$/\1 prometheus-client/' Dockerfile
sed 's/"-w", "4"/"-w", "1"/' Dockerfile > Dockerfile1w
docker build -f Dockerfile1w -t amigos:3.0 .
cd ..

# 6. lanza-flask3.sh (copia de lanza-flask.sh con la imagen 3.0)
sed 's/amigos:[0-9.]*/amigos:3.0/' lanza-flask.sh > lanza-flask3.sh
chmod +x lanza-*.sh

# 7. Relanzar: base de datos (si no corre), amigos y nginx (nginx después: resuelve "amigos" al arrancar)
docker ps --format '{{.Names}}' | grep -qx basedatos || { ./lanza-basedatos.sh; sleep 8; }
docker rm -f amigos nginx 2>/dev/null || true
./lanza-flask3.sh
sleep 3
./lanza-nginx.sh
sleep 2
curl -si http://127.0.0.1/health | head -1
curl -s http://127.0.0.1/metrics | grep -m1 amigos_http_requests_total
