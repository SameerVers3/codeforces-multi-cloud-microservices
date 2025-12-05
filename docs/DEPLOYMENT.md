# Deployment Guide

## Prerequisites

- Terraform >= 1.0
- kubectl
- Docker
- AWS CLI, Azure CLI, GCP CLI configured
- Kubernetes clusters access

## Multi-Cloud Deployment

### 1. AWS Deployment (Execution & Submission Services)

```bash
cd infrastructure/terraform/aws
terraform init
terraform plan
terraform apply
```

### 2. Azure Deployment (Auth, Contest, Database)

```bash
cd infrastructure/terraform/azure
terraform init
terraform plan -var="db_admin_login=admin" -var="db_admin_password=secure_password"
terraform apply
```

### 3. GCP Deployment (Scoring, Leaderboard, Frontend)

```bash
cd infrastructure/terraform/gcp
terraform init
terraform plan -var="gcp_project_id=your-project-id"
terraform apply
```

## Kubernetes Deployment

After infrastructure is provisioned:

```bash
# Configure kubectl for each cluster
aws eks update-kubeconfig --name codeforces-aws-cluster --region us-east-1
az aks get-credentials --resource-group codeforces-rg --name codeforces-aks-cluster
gcloud container clusters get-credentials codeforces-gke-cluster --region us-central1

# Deploy services
kubectl apply -f infrastructure/kubernetes/base/
```

## CI/CD Pipeline

The GitHub Actions pipeline automatically:
1. Builds Docker images for all services
2. Scans images for vulnerabilities
3. Deploys to respective cloud providers
4. Updates Kubernetes deployments

## Monitoring

Access Prometheus and Grafana dashboards:
- Prometheus: `http://prometheus-service:9090`
- Grafana: `http://grafana-service:3000`

## Health Checks

All services expose `/health` endpoints:
- Auth Service: `http://auth-service:8000/health`
- Contest Service: `http://contest-service:8000/health`
- Submission Service: `http://submission-service:8000/health`
- Execution Service: `http://execution-service:8000/health`
- Scoring Service: `http://scoring-service:8000/health`
- Leaderboard Service: `http://leaderboard-service:8000/health`

