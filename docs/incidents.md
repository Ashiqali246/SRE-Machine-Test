# Incident Simulation and RCA Report

This document shows the failure scenarios performed for the SRE machine test. Three scenarios were tested:

1. Pod CrashLoopBackOff
2. High CPU
3. Excess logging / log flood

The tests were performed in the `sre-app` namespace on the k3s cluster.

---

# Incident 1: Pod CrashLoopBackOff

## Objective

Simulate a corrupted application startup configuration that causes a container to repeatedly fail and enter `CrashLoopBackOff`.

## Reproduction

The test manifest is available at:

`tests/crashloop.yaml`

Apply the failure:

```bash
kubectl apply -f tests/crashloop.yaml
kubectl get pod crashloop-test -n sre-app -w
```

---

# Incident 2: High CPU

## Objective

Generate more CPU load and verify that Kubernetes and the monitoring stack can detect abnormal resource consumption.

## Reproduction

The test manifest is available at:

`tests/cpu-stress.yaml`

Apply the failure:

```bash
kubectl apply -f tests/cpu-stress.yaml
kubectl get pods -n sre-app
```

---

# Incident 3: Log Flood

## Objective

Generate a controlled burst of application logs and validate log collection through Promtail, Loki and Grafana.

## Reproduction

The test manifest is available at:

`tests/log-flood.sh`

To run:

```bash
./tests/log-flood.sh
```

Logs were viewed in Grafana using the Loki datasource with:

**LogQL**

```logql
{namespace="sre-app", container="sre-test-app"} |= "GET /health"
```

## Detection and Evidence

Application health was verified with:

```bash
curl -H "Host: sre-app.local" http://localhost/health
```

The application remained healthy during the test.

Logs were viewed in Grafana using the Loki datasource with:

```logql
{namespace="sre-app", container="sre-test-app"} |= "GET /health"
```

A large burst of `/health` request logs was visible, confirming that Promtail successfully collected the logs and Loki successfully ingested them.

## Incident Timeline

| Stage | Observation |
|---|---|
| Failure introduced | 2,000 HTTP requests generated |
| Detection | Significant increase in application log volume |
| Investigation | Loki logs inspected through Grafana |
| Root cause identified | Controlled request/log flood |
| Mitigation | Request generation stopped |
| Recovery | Log volume returned to normal |

## Root Cause

A controlled burst of HTTP requests generated a large number of Gunicorn access-log entries within a short period.

## 5 Whys

**Why did log volume increase?**  
A large number of HTTP requests were generated.

**Why did each request create logs?**  
Gunicorn access logging was enabled.

**Why were the logs collected centrally?**  
Promtail was configured to collect Kubernetes container logs.

**Why were they visible in Grafana?**  
Promtail shipped the logs to Loki, which was configured as a Grafana datasource.

**Why could excessive logging become a problem?**  
Sustained high-volume logging can increase storage usage and ingestion/query load.

## Mitigation and Recovery

The request-generation process completed/stopped, after which application log volume returned to its normal level.

No application restart was required.

## Corrective / Preventive Actions

- Configure appropriate Loki retention.
- Monitor Loki storage consumption.
- Avoid unnecessary verbose logging in production.
- Apply rate limiting where appropriate.
- Alert on abnormal log-volume growth.

**Owner:** DevOps/SRE Team  
**Remediation timeline:** Immediate traffic/log-source investigation; retention and logging-policy review within the next maintenance cycle.
