# Security and Secrets Management

This document describes the basic security practices used in the SRE machine test implementation.

## 1. Secrets Management

Sensitive credentials are not hardcoded in the application source code or committed to the Git repository.

GitHub Actions Secrets are used for CI/CD credentials such as:

- Docker Hub username/token
- Deployment server details
- SSH deployment credentials

Kubernetes Secrets are used for sensitive application runtime configuration.

Non-sensitive application configuration is stored using Kubernetes ConfigMaps.

## 2. Git Repository Security

The repository uses `.gitignore` to prevent sensitive or unnecessary files from being committed.

The following must never be committed:

- Personal Access Tokens (PAT)
- Passwords
- Docker Hub tokens
- SSH private keys
- Kubernetes kubeconfig files
- Production secret values

The repository will be checked for exposed credentials before final submission.

## 3. Kubernetes Security

The application uses:

- Separate Kubernetes namespaces
- Kubernetes Secrets for sensitive configuration
- Resource requests and limits
- Liveness and readiness probes
- ClusterIP service for internal application exposure
- Traefik Ingress for controlled HTTP access

For a production environment, Kubernetes RBAC should follow the principle of least privilege.

## 4. Container Security

Application containers should:

- Use trusted base images
- Avoid storing credentials inside images
- Use fixed/versioned image tags
- Define CPU and memory limits
- Be scanned for known vulnerabilities before production deployment

The CI/CD pipeline creates versioned application images using the Git commit SHA.

## 5. Network Security

The application is exposed through Traefik Ingress rather than directly exposing application pods.

In a production environment, additional controls should include:

- TLS/HTTPS
- Kubernetes NetworkPolicies
- Restricted security groups/firewall rules
- Private networking where appropriate

## 6. Monitoring and Logging Security

Prometheus, Grafana and Loki should not be publicly exposed without authentication and network restrictions.

Sensitive values should not be written to application logs.

Log retention should be configured according to operational and security requirements.

## 7. Production Recommendations

For a production deployment:

- Use least-privilege RBAC
- Enable TLS
- Rotate credentials regularly
- Use a dedicated secrets-management solution where appropriate
- Scan container images
- Apply Kubernetes NetworkPolicies
- Keep k3s, Helm charts and container images updated
- Restrict administrative access to monitoring systems

These controls reduce the risk of credential exposure, unauthorized access and insecure workload configuration.
