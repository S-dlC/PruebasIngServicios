#!/bin/bash
# Práctica 2.3: instala Node Exporter, Prometheus, Alertmanager y Grafana en la VM.
# Uso: bash monitor_instalar.sh   (usuario con sudo; ejecutar en la carpeta del proyecto)
set -e
NE=1.12.1; PROM=3.15.0; AM=0.29.0
START=$(pwd)
cd /tmp

mkuser() { id "$1" >/dev/null 2>&1 || sudo useradd --no-create-home --shell /bin/false "$1"; }

# ---------- Node Exporter ----------
wget -q https://github.com/prometheus/node_exporter/releases/download/v$NE/node_exporter-$NE.linux-amd64.tar.gz
tar xzf node_exporter-$NE.linux-amd64.tar.gz
sudo cp node_exporter-$NE.linux-amd64/node_exporter /usr/local/bin/
mkuser node_exporter
sudo tee /etc/systemd/system/node_exporter.service >/dev/null <<'EOF'
[Unit]
Description=Prometheus Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
EOF

# ---------- Prometheus ----------
wget -q https://github.com/prometheus/prometheus/releases/download/v$PROM/prometheus-$PROM.linux-amd64.tar.gz
tar xzf prometheus-$PROM.linux-amd64.tar.gz
sudo cp prometheus-$PROM.linux-amd64/{prometheus,promtool} /usr/local/bin/
mkuser prometheus
sudo mkdir -p /etc/prometheus /var/lib/prometheus
sudo chown prometheus:prometheus /var/lib/prometheus

sudo tee /etc/prometheus/prometheus.yml >/dev/null <<'EOF'
global:
  scrape_interval: 15s

rule_files:
  - "/etc/prometheus/alerts.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - "localhost:9093"

scrape_configs:
  - job_name: "amigos"
    static_configs:
      - targets: ["localhost"]

  - job_name: "node"
    static_configs:
      - targets: ["localhost:9100"]
EOF

sudo tee /etc/prometheus/alerts.yml >/dev/null <<'EOF'
groups:
  - name: amigos
    rules:
      - alert: AmigosDown
        expr: up{job="amigos"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Amigos no está disponible"
          description: "Prometheus no puede acceder al servicio Amigos desde hace más de 1 minuto."
      - alert: AmigosHighErrorRate
        expr: rate(amigos_http_errors_total[5m]) > 0
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: "Amigos está generando errores HTTP"
          description: "El servicio Amigos está devolviendo respuestas HTTP de error."
EOF
promtool check config /etc/prometheus/prometheus.yml
promtool check rules /etc/prometheus/alerts.yml

sudo tee /etc/systemd/system/prometheus.service >/dev/null <<'EOF'
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/usr/local/bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/var/lib/prometheus

[Install]
WantedBy=multi-user.target
EOF

# ---------- Alertmanager ----------
wget -q https://github.com/prometheus/alertmanager/releases/download/v$AM/alertmanager-$AM.linux-amd64.tar.gz
tar xzf alertmanager-$AM.linux-amd64.tar.gz
sudo cp alertmanager-$AM.linux-amd64/{alertmanager,amtool} /usr/local/bin/
mkuser alertmanager
sudo mkdir -p /etc/alertmanager /var/lib/alertmanager
sudo tee /etc/alertmanager/alertmanager.yml >/dev/null <<'EOF'
global:

route:
  receiver: "default"

receivers:
  - name: "default"
EOF
sudo chown -R alertmanager:alertmanager /etc/alertmanager /var/lib/alertmanager
sudo tee /etc/systemd/system/alertmanager.service >/dev/null <<'EOF'
[Unit]
Description=Prometheus Alertmanager
Wants=network-online.target
After=network-online.target

[Service]
User=alertmanager
Group=alertmanager
Type=simple
ExecStart=/usr/local/bin/alertmanager \
  --config.file=/etc/alertmanager/alertmanager.yml \
  --storage.path=/var/lib/alertmanager

[Install]
WantedBy=multi-user.target
EOF

# ---------- Grafana (con datasource y dashboard provisionados) ----------
sudo apt-get install -y apt-transport-https software-properties-common wget
sudo mkdir -p /etc/apt/keyrings
wget -q -O - https://apt.grafana.com/gpg.key | sudo gpg --dearmor --yes -o /etc/apt/keyrings/grafana.gpg
echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
sudo apt-get update
sudo apt-get install -y grafana

sudo tee /etc/grafana/provisioning/datasources/prometheus.yml >/dev/null <<'EOF'
apiVersion: 1
datasources:
  - name: Prometheus
    uid: prometheus
    type: prometheus
    access: proxy
    url: http://localhost:9090
    isDefault: true
EOF
sudo tee /etc/grafana/provisioning/dashboards/amigos.yml >/dev/null <<'EOF'
apiVersion: 1
providers:
  - name: amigos
    type: file
    options:
      path: /var/lib/grafana/dashboards
EOF

# dashboard.json (queda también en la carpeta del proyecto, para el repositorio)
cat > "$START/dashboard.json" <<'EOF'
{"title":"Amigos","uid":"amigos","schemaVersion":39,"refresh":"10s","time":{"from":"now-30m","to":"now"},"panels":[
{"id":1,"type":"timeseries","title":"Peticiones HTTP de Amigos","datasource":{"type":"prometheus","uid":"prometheus"},"gridPos":{"x":0,"y":0,"w":12,"h":8},"targets":[{"refId":"A","expr":"amigos_http_requests_total"}]},
{"id":2,"type":"timeseries","title":"Peticiones por segundo","datasource":{"type":"prometheus","uid":"prometheus"},"gridPos":{"x":12,"y":0,"w":12,"h":8},"targets":[{"refId":"A","expr":"rate(amigos_http_requests_total[5m])"}]},
{"id":3,"type":"timeseries","title":"Errores HTTP por segundo","datasource":{"type":"prometheus","uid":"prometheus"},"gridPos":{"x":0,"y":8,"w":12,"h":8},"targets":[{"refId":"A","expr":"rate(amigos_http_errors_total[5m])"}]},
{"id":4,"type":"timeseries","title":"Tiempo medio de respuesta (s)","datasource":{"type":"prometheus","uid":"prometheus"},"gridPos":{"x":12,"y":8,"w":12,"h":8},"targets":[{"refId":"A","expr":"rate(amigos_http_request_duration_seconds_sum[5m]) / rate(amigos_http_request_duration_seconds_count[5m])"}]},
{"id":5,"type":"timeseries","title":"Memoria disponible (GB)","datasource":{"type":"prometheus","uid":"prometheus"},"gridPos":{"x":0,"y":16,"w":12,"h":8},"targets":[{"refId":"A","expr":"node_memory_MemAvailable_bytes / 1024 / 1024 / 1024"}]},
{"id":6,"type":"timeseries","title":"Utilización CPU (%)","datasource":{"type":"prometheus","uid":"prometheus"},"gridPos":{"x":12,"y":16,"w":12,"h":8},"targets":[{"refId":"A","expr":"100 * (1 - avg(rate(node_cpu_seconds_total{mode=\"idle\"}[5m])))"}]}
]}
EOF
sudo mkdir -p /var/lib/grafana/dashboards
sudo cp "$START/dashboard.json" /var/lib/grafana/dashboards/
sudo chown -R grafana:grafana /var/lib/grafana/dashboards

# ---------- Arranque y habilitación ----------
sudo systemctl daemon-reload
sudo systemctl enable --now node_exporter prometheus alertmanager grafana-server
sleep 5
systemctl is-active node_exporter prometheus alertmanager grafana-server
echo "Prometheus :9090 | Alertmanager :9093 | Grafana :3000 (admin/admin) | Node Exporter :9100"
