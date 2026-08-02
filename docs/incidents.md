# Incident Simulation and RCA Report

This document describes the failure scenarios simulated as part of the **SRE Machine Test**. The following three incident scenarios were tested:

1. Pod `CrashLoopBackOff`
2. High CPU Usage
3. Excessive Logging / Log Flood

All tests were performed in the `sre-app` namespace on the **K3s cluster**.

---

# Incident 1: Pod CrashLoopBackOff

## Objective

Simulate a corrupted application startup configuration that causes a container to repeatedly fail and enter the `CrashLoopBackOff` state.

## Reproduction

The test manifest is available at:

```text
tests/crashloop.yaml
```

Apply the failure scenario:

```bash
kubectl apply -f tests/crashloop.yaml
kubectl get pod crashloop-test -n sre-app -w
```

---

# Incident 2: High CPU Usage

## Objective

Generate high CPU load and verify that Kubernetes and the monitoring stack can detect abnormal resource consumption.

## Reproduction

The test manifest is available at:

```text
tests/cpu-stress.yaml
```

Apply the failure scenario:

```bash
kubectl apply -f tests/cpu-stress.yaml
kubectl get pods -n sre-app
```

---

# Incident 3: Log Flood

## Objective

Generate a controlled burst of application logs and validate that the logs are successfully collected and visualized through **Promtail, Loki, and Grafana**.

## Reproduction

The test script is available at:

```text
tests/log-flood.sh
```

Run the script:

```bash
./tests/log-flood.sh
```

## Log Verification

The generated logs were verified in **Grafana** using the **Loki** data source.

The following LogQL query was used to filter the application health-check logs:

```logql
{namespace="sre-app", container="sre-test-app"} |= "GET /health"
```
