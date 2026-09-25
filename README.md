cat > README.md <<'EOF'
# Kubewatch

A Python microservices project deployed on Kubernetes with monitoring, alerting and autoscaling.

## Stack

- FastAPI
- Celery + Redis
- Docker
- Kubernetes
- Helm
- Prometheus + Grafana
- Locust

## What I built

- Containerized FastAPI API and Celery worker
- Deployed services to Kubernetes
- Added NGINX Ingress
- Added Prometheus metrics and Grafana monitoring
- Added API failure alerts
- Added HPA for automatic scaling
- Tested autoscaling with Locust

## Autoscaling

Under load, the API scaled:

`2 → 4 → 8 pods`

After the load stopped:

`8 → 2 pods`


For Docker: 
docker compose up --build

For kubernetes: 
helm upgrade --install kubewatch ./helm --set api.image.tag=v2
