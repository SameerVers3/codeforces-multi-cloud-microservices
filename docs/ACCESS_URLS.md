# Access URLs Guide

## Overview

After deployment, your services are accessible via Kubernetes LoadBalancers. Here's how to find and access them.

## 🚀 Quick Access - Get Your URLs

### Step 1: Get Frontend URL (AWS EKS)

```bash
# Configure kubectl for AWS
aws eks update-kubeconfig --name codeforces-aws-cluster --region us-east-1

# Get frontend external URL
kubectl get service frontend -n codeforces -o jsonpath='{.status.loadBalancer.ingress[0].hostname}' && echo
# OR for IP:
kubectl get service frontend -n codeforces -o jsonpath='{.status.loadBalancer.ingress[0].ip}' && echo
```

**Frontend URL**: `http://<EXTERNAL-IP-OR-HOSTNAME>`

### Step 2: Get Backend Service URLs (Azure AKS)

```bash
# Configure kubectl for Azure
az aks get-credentials --resource-group codeforces-rg --name codeforces-aks-cluster

# Get auth service external IP
kubectl get service auth-service -n codeforces -o jsonpath='{.status.loadBalancer.ingress[0].ip}' && echo

# Get contest service external IP
kubectl get service contest-service -n codeforces -o jsonpath='{.status.loadBalancer.ingress[0].ip}' && echo
```

**Auth Service URL**: `http://<EXTERNAL-IP>/api/v1/auth`  
**Contest Service URL**: `http://<EXTERNAL-IP>/api/v1/contests`

### Step 3: View All Service URLs

```bash
# AWS EKS - All services
aws eks update-kubeconfig --name codeforces-aws-cluster --region us-east-1
kubectl get services -n codeforces

# Azure AKS - All services  
az aks get-credentials --resource-group codeforces-rg --name codeforces-aks-cluster
kubectl get services -n codeforces
```

## Quick Access Commands

### AWS EKS Cluster

```bash
# Configure kubectl for AWS
aws eks update-kubeconfig --name codeforces-aws-cluster --region us-east-1

# Get all services and their external IPs
kubectl get services -n codeforces

# Get specific service external IP
kubectl get service frontend -n codeforces
kubectl get service execution-service -n codeforces
```

### Azure AKS Cluster

```bash
# Configure kubectl for Azure
az aks get-credentials --resource-group codeforces-rg --name codeforces-aks-cluster

# Get all services and their external IPs
kubectl get services -n codeforces

# Get specific service external IP
kubectl get service auth-service -n codeforces
kubectl get service contest-service -n codeforces
```

## Service URLs

### Exposed Services (LoadBalancer)

| Service | Cloud | Type | Access |
|---------|-------|------|--------|
| **Frontend** | AWS EKS | LoadBalancer | External URL |
| **Auth Service** | Azure AKS | LoadBalancer | External IP |
| **Contest Service** | Azure AKS | LoadBalancer | External IP |
| Submission Service | AWS EKS | ClusterIP | Internal only |
| Execution Service | AWS EKS | ClusterIP | Internal only |
| Scoring Service | AWS EKS | ClusterIP | Internal only |
| Leaderboard Service | AWS EKS | ClusterIP | Internal only |

### Internal Services

Backend services (Submission, Execution, Scoring, Leaderboard) remain as `ClusterIP` and are accessed internally by the frontend. They don't need external access.

### Alternative: Port Forwarding (For Testing Only)

```bash
# AWS EKS - Frontend
kubectl port-forward -n codeforces service/frontend 3000:80

# AWS EKS - Execution Service
kubectl port-forward -n codeforces service/execution-service 8004:80

# Azure AKS - Auth Service
kubectl port-forward -n codeforces service/auth-service 8001:80

# Azure AKS - Contest Service
kubectl port-forward -n codeforces service/contest-service 8002:80
```

Then access:
- Frontend: `http://localhost:3000`
- Auth Service: `http://localhost:8001`
- Contest Service: `http://localhost:8002`
- Execution Service: `http://localhost:8004`

### Using Ingress (Future Enhancement)

For production with custom domains and SSL, consider setting up an Ingress controller:

Set up an Ingress controller (e.g., NGINX Ingress) to route traffic to services.

## Service Endpoints

### AWS EKS Cluster
- **Cluster Endpoint**: `https://8965435893067B5893B51D4061489B8E.gr7.us-east-1.eks.amazonaws.com`
- **Cluster ID**: `codeforces-aws-cluster`
- **VPC ID**: `vpc-0b68eb4a3b4c09829`

### Azure AKS Cluster
- **Cluster FQDN**: Check with `kubectl cluster-info` or Azure Portal
- **Load Balancer IP**: `20.185.89.222` (from Terraform output)

## Service Ports

| Service | Port | Cloud | Access Method |
|---------|------|-------|---------------|
| Frontend | 80 | AWS | Port-forward or LoadBalancer |
| Auth Service | 80 | Azure | Port-forward or LoadBalancer |
| Contest Service | 80 | Azure | Port-forward or LoadBalancer |
| Submission Service | 80 | AWS | Port-forward or LoadBalancer |
| Execution Service | 80 | AWS | Port-forward or LoadBalancer |
| Scoring Service | 80 | AWS | Port-forward or LoadBalancer |
| Leaderboard Service | 80 | AWS | Port-forward or LoadBalancer |

## Get External IPs

### For LoadBalancer Services

```bash
# AWS EKS
kubectl get services -n codeforces -o wide

# Azure AKS
kubectl get services -n codeforces -o wide
```

Look for services with `TYPE=LoadBalancer` and check the `EXTERNAL-IP` column.

## Example: Get Frontend URL

```bash
# On AWS EKS
kubectl get service frontend -n codeforces -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'

# On Azure AKS
kubectl get service frontend -n codeforces -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

## Health Check URLs

Once you have the external IPs, test health endpoints:

```bash
# Frontend (if LoadBalancer)
curl http://<EXTERNAL-IP>/health

# Auth Service
curl http://<EXTERNAL-IP>/health

# Contest Service
curl http://<EXTERNAL-IP>/health
```

## Production Setup

For production, consider:

1. **Ingress Controller**: Set up NGINX Ingress or similar
2. **Domain Name**: Point a domain to the load balancer IP
3. **SSL/TLS**: Configure HTTPS with Let's Encrypt
4. **API Gateway**: Use AWS API Gateway or Azure API Management

## Current Status

- ✅ **AWS EKS**: Cluster created, services deployed
- ✅ **Azure AKS**: Cluster exists, services deployed
- ✅ **Frontend**: LoadBalancer (external access enabled)
- ✅ **Auth Service**: LoadBalancer (external access enabled)
- ✅ **Contest Service**: LoadBalancer (external access enabled)
- ✅ **Backend Services**: ClusterIP (internal, accessed via frontend)

## 📝 Getting URLs After Deployment

After the next deployment, run these commands to get your URLs:

```bash
# Frontend URL (AWS)
aws eks update-kubeconfig --name codeforces-aws-cluster --region us-east-1
FRONTEND_URL=$(kubectl get service frontend -n codeforces -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
echo "Frontend: http://$FRONTEND_URL"

# Auth Service URL (Azure)
az aks get-credentials --resource-group codeforces-rg --name codeforces-aks-cluster
AUTH_IP=$(kubectl get service auth-service -n codeforces -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo "Auth Service: http://$AUTH_IP"

# Contest Service URL (Azure)
CONTEST_IP=$(kubectl get service contest-service -n codeforces -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo "Contest Service: http://$CONTEST_IP"
```

**Note**: LoadBalancer IPs may take 2-5 minutes to provision after deployment.

## Quick Commands Summary

```bash
# Switch to AWS context
aws eks update-kubeconfig --name codeforces-aws-cluster --region us-east-1

# Switch to Azure context
az aks get-credentials --resource-group codeforces-rg --name codeforces-aks-cluster

# View all services
kubectl get services -n codeforces

# Port forward frontend
kubectl port-forward -n codeforces service/frontend 3000:80
```

Then access at `http://localhost:3000`

