# SRE Machine Test

This project demonstrates the deployment and operation of a containerized microservice on a lightweight Kubernetes (k3s) environment with CI/CD, monitoring, centralized logging, alerting and controlled failure simulations.

## Architecture

```text
                         GitHub Repository
                                |
                                v
                         GitHub Actions
                                |
                     Build & Push Docker Image
                                |
                                v
                           Docker Hub
                                |
                                v
+----------------------------------------------------------+
|                     Linux EC2 VM                         |
|                                                          |
|                         k3s                              |
|                                                          |
|   Traefik Ingress                                        |
|          |                                               |
|          v                                               |
|   Kubernetes Service                                     |
|          |                                               |
|          v                                               |
|   sre-test-app (2 replicas)                              |
|          |                                               |
|          +-----------> /metrics ---> Prometheus           |
|          |                              |                |
|          |                              v                |
|          |                           Grafana              |
|          |                                               |
|          +-- container logs --> Promtail --> Loki         |
|                                           |              |
|                                           v              |
|                                        Grafana            |
+----------------------------------------------------------+
```

## Technology Stack

- Linux / AWS EC2
- Docker
- k3s Kubernetes
- Helm
- Traefik Ingress
- GitHub Actions
- Docker Hub
- Prometheus
- Grafana
- Alertmanager
- Loki
- Promtail
- Python / Gunicorn

## Application

The application exposes the following endpoints:

| Endpoint | Purpose |
|---|---|
| `/` | Application information |
| `/health` | Liveness/health check |
| `/ready` | Readiness check |
| `/metrics` | Prometheus metrics |

The application runs using Gunicorn on port `5000`.

## Kubernetes Deployment

The application is deployed using a custom Helm chart.

The Helm chart contains:

- Deployment
- ClusterIP Service
- ConfigMap
- Kubernetes Secret
- Traefik Ingress
- ServiceMonitor
- Resource requests and limits
- Liveness probe
- Readiness probe

The normal application deployment runs with two replicas.

Application namespace:

```text
sre-app
```

Verify the deployment:

```bash
kubectl get pods -n sre-app
kubectl get deployment -n sre-app
kubectl get svc -n sre-app
kubectl get ingress -n sre-app
```

Test the application:

```bash
curl -H "Host: sre-app.local" http://localhost/
curl -H "Host: sre-app.local" http://localhost/health
```

## Helm Deployment

Validate the chart:

```bash
cd helm/sre-test-app
helm lint .
```

Deploy:

```bash
helm upgrade --install sre-test-app . \
  --namespace sre-app \
  --create-namespace \
  --set appSecret='<runtime-secret>'
```

Sensitive runtime values should not be committed to the repository.

## CI/CD

GitHub Actions provides the CI/CD pipeline.

The workflow:

1. Checks out the source code.
2. Builds the Docker image.
3. Tags the image using the Git commit SHA.
4. Authenticates to Docker Hub using GitHub Secrets.
5. Pushes the image to Docker Hub.
6. Connects to the deployment server.
7. Deploys the new image to k3s using Helm.
8. Verifies the Kubernetes rollout.

CI/CD configuration is located at:

```text
.github/workflows/deploy.yml
```

Credentials required by the workflow are stored using GitHub Actions Secrets and are not committed to the repository.

## Monitoring

The monitoring stack is deployed using `kube-prometheus-stack`.

Components include:

- Prometheus
- Grafana
- Alertmanager
- kube-state-metrics
- node-exporter
- Prometheus Operator

Application metrics are exposed through:

```text
/metrics
```

A Kubernetes ServiceMonitor allows Prometheus to discover and scrape the application.

Example application metric:

```promql
sre_app_requests_total
```

### Grafana

Two Grafana dashboards were created to provide application and Kubernetes monitoring visibility.

Grafana uses Prometheus as the metrics datasource.

Dashboard JSON files are stored with the monitoring configuration in this repository.

## Alerting

Prometheus alerting/recording rules include:

- `SREAppDown`
- `SREAppPodRestarting`
- `SREAppHighCPU`
- `sre_app:request_rate:5m` recording rule

Rules can be verified through Prometheus or Grafana.

Example:

```bash
curl -s http://localhost:9090/api/v1/rules | jq
```

## Centralized Logging

Centralized Kubernetes logging is implemented using:

```text
Application
    |
    v
Kubernetes container logs
    |
    v
Promtail
    |
    v
Loki
    |
    v
Grafana
```

Loki and Promtail run in the `logging` namespace.

Verify:

```bash
kubectl get pods -n logging
kubectl get daemonset -n logging
```

Application logs can be queried in Grafana using the Loki datasource:

```logql
{namespace="sre-app", container="sre-test-app"}
```

## Failure Simulations

Three controlled failure scenarios were performed.

### 1. Pod CrashLoopBackOff

A container with intentionally invalid startup configuration was created:

```bash
kubectl apply -f tests/crashloop.yaml
kubectl get pod crashloop-test -n sre-app -w
```

Troubleshooting:

```bash
kubectl logs crashloop-test -n sre-app
kubectl describe pod crashloop-test -n sre-app
```

Cleanup:

```bash
kubectl delete pod crashloop-test -n sre-app
```

### 2. High CPU

A controlled CPU-intensive workload was deployed:

```bash
kubectl apply -f tests/cpu-stress.yaml
kubectl top pods -n sre-app
```

CPU usage can also be observed using Prometheus/Grafana.

Cleanup:

```bash
kubectl delete deployment cpu-stress -n sre-app
```

### 3. Excess Logging / Log Flood

Generate a controlled burst of application requests:

```bash
./tests/log-flood.sh
```

The resulting logs can be observed using Loki in Grafana:

```logql
{namespace="sre-app", container="sre-test-app"} |= "GET /health"
```

Detailed incident timelines, evidence, root-cause analysis and 5-Why analysis are documented in:

```text
docs/incidents.md
```

## Operations Runbook

Common operational procedures including pod troubleshooting, resource investigation, restart, scaling and rollback are documented in:

```text
docs/runbook.md
```

## Security

Security and secrets-management practices are documented in:

```text
docs/security.md
```

Important principles include:

- No credentials committed to Git.
- CI/CD credentials stored in GitHub Secrets.
- Runtime secrets stored using Kubernetes Secrets.
- Resource limits configured for workloads.
- Least-privilege RBAC recommended for production.
- TLS and NetworkPolicies recommended for production.
- Monitoring services should not be publicly exposed without protection.

## Setup Summary

A high-level setup sequence is:

1. Provision Linux VM.
2. Install Docker, kubectl, Helm and k3s.
3. Clone the repository.
4. Configure required GitHub Actions Secrets.
5. Deploy the application using Helm.
6. Install `kube-prometheus-stack`.
7. Apply the application ServiceMonitor and alerting rules.
8. Install Loki and Promtail.
9. Configure Loki as a Grafana datasource.
10. Import/use the Grafana dashboards.
11. Verify application metrics and centralized logs.

## Teardown

Remove the application:

```bash
helm uninstall sre-test-app -n sre-app
```

Remove monitoring:

```bash
helm uninstall monitoring -n monitoring
```

Remove Loki and Promtail:

```bash
helm uninstall promtail -n logging
helm uninstall loki -n logging
```

Namespaces can be removed when no longer required:

```bash
kubectl delete namespace sre-app
kubectl delete namespace monitoring
kubectl delete namespace logging
```

## Incident Documentation

Full incident simulation and RCA documentation:

```text
docs/incidents.md
```

Operational runbook:

```text
docs/runbook.md
```

Security documentation:

```text
docs/security.md
```

## Assumptions and Design Decisions

- A single Linux EC2 VM is used for the lightweight k3s environment.
- Traefik bundled with k3s is used as the ingress controller.
- The application uses two replicas during normal operation.
- Local-path storage is used for persistent monitoring/logging data in this assessment environment.
- Failure simulations are controlled test workloads and are removed after evidence is collected.
- The environment is designed for assessment/demo purposes. Production deployment would require additional high availability, TLS, RBAC, network policies, backup and security controls.

## Result

The implementation demonstrates:

- Containerized application deployment
- Kubernetes orchestration using k3s
- Helm-based application management
- Automated CI/CD using GitHub Actions
- Prometheus metrics collection
- Grafana dashboards
- Prometheus alerting
- Centralized logging using Loki and Promtail
- Controlled SRE failure simulations
- Incident investigation and RCA
- Operational recovery procedures
