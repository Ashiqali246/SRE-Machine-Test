# SRE Operations Runbook

This runbook provides basic operational and recovery procedures for the SRE test application running on k3s.

## 1. Check Cluster Health

```bash
kubectl get nodes
kubectl get pods -A
