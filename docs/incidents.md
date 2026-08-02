# Incident Simulation and RCA Report

This document shows th failure scenarios performed for the SRE machine test. Three scenarios were tested:

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
