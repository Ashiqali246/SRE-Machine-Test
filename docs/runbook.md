# SRE Operations Runbook

This runbook provides basic operational and recovery procedures for the SRE test application running on k3s.

## 1. Check Cluster Health

```bash
kubectl get nodes
kubectl get pods -A
```

## 4. CrashLoopBackOff

```bash
kubectl get pods -n sre-app
kubectl logs <pod-name> -n sre-app
kubectl describe pod <pod-name> -n sre-app
```

## 5. High CPU / Memory

Check current usage:

```bash
kubectl top pods -n sre-app
kubectl top nodes
```

## 6. Application Logs

```bash
kubectl logs -n sre-app -l app=sre-test-app --tail=100
```

Centralized logs can also be viewed in Grafana using Loki:

```logql
{namespace="sre-app", container="sre-test-app"}
```

## 7. Monitoring

Check monitoring components:

```bash
kubectl get pods -n monitoring
```

## 8. Logging Stack

```bash
kubectl get pods -n logging
kubectl get daemonset -n logging
```

Check Promtail:

```bash
kubectl logs -n logging -l app.kubernetes.io/name=promtail --tail=50
```

Check Loki:

```bash
curl -s http://localhost:3100/loki/api/v1/labels | jq
```
