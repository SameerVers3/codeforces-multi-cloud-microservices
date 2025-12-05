# How to Get Your Deployment URLs

## 🎯 Quick Commands

After deployment completes, run these commands to get your URLs:

### Frontend URL (AWS EKS)

```bash
# Connect to AWS cluster
aws eks update-kubeconfig --name codeforces-aws-cluster --region us-east-1

# Get frontend URL (may take 2-5 minutes to provision)
kubectl get service frontend -n codeforces

# Or get just the URL:
kubectl get service frontend -n codeforces -o jsonpath='{.status.loadBalancer.ingress[0].hostname}' && echo
# If hostname is empty, try IP:
kubectl get service frontend -n codeforces -o jsonpath='{.status.loadBalancer.ingress[0].ip}' && echo
```

**Access**: `http://<EXTERNAL-IP-OR-HOSTNAME>`

### Auth Service URL (Azure AKS)

```bash
# Connect to Azure cluster
az aks get-credentials --resource-group codeforces-rg --name codeforces-aks-cluster

# Get auth service URL
kubectl get service auth-service -n codeforces

# Or get just the IP:
kubectl get service auth-service -n codeforces -o jsonpath='{.status.loadBalancer.ingress[0].ip}' && echo
```

**Access**: `http://<EXTERNAL-IP>/api/v1/auth`

### Contest Service URL (Azure AKS)

```bash
# (Already connected from above)
kubectl get service contest-service -n codeforces

# Or get just the IP:
kubectl get service contest-service -n codeforces -o jsonpath='{.status.loadBalancer.ingress[0].ip}' && echo
```

**Access**: `http://<EXTERNAL-IP>/api/v1/contests`

## 📋 All URLs at Once

```bash
#!/bin/bash

echo "=== AWS EKS Services ==="
aws eks update-kubeconfig --name codeforces-aws-cluster --region us-east-1
echo "Frontend:"
kubectl get service frontend -n codeforces -o jsonpath='  http://{.status.loadBalancer.ingress[0].hostname}{"\n"}' || \
kubectl get service frontend -n codeforces -o jsonpath='  http://{.status.loadBalancer.ingress[0].ip}{"\n"}'

echo ""
echo "=== Azure AKS Services ==="
az aks get-credentials --resource-group codeforces-rg --name codeforces-aks-cluster
echo "Auth Service:"
kubectl get service auth-service -n codeforces -o jsonpath='  http://{.status.loadBalancer.ingress[0].ip}/api/v1/auth{"\n"}'
echo "Contest Service:"
kubectl get service contest-service -n codeforces -o jsonpath='  http://{.status.loadBalancer.ingress[0].ip}/api/v1/contests{"\n"}'
```

## ⏱️ LoadBalancer Provisioning Time

- **AWS**: 2-5 minutes (creates ELB)
- **Azure**: 2-5 minutes (uses existing public IP: `20.185.89.222`)

If you see `<pending>` in the EXTERNAL-IP column, wait a few minutes and check again.

## 🔍 Check Service Status

```bash
# AWS
kubectl get services -n codeforces

# Azure
kubectl get services -n codeforces
```

Look for services with `TYPE=LoadBalancer` and check the `EXTERNAL-IP` column.

## 📝 Example Output

After running `kubectl get services -n codeforces`, you should see:

```
NAME                TYPE           CLUSTER-IP      EXTERNAL-IP                              PORT(S)        AGE
frontend            LoadBalancer   10.100.0.10     a1b2c3d4e5f6.us-east-1.elb.amazonaws.com  80:30000/TCP   5m
auth-service        LoadBalancer   10.100.0.20     20.185.89.222                            80:30001/TCP   5m
contest-service     LoadBalancer   10.100.0.30     20.185.89.223                            80:30002/TCP   5m
```

## 🚀 Next Steps

1. **Wait for LoadBalancer provisioning** (2-5 minutes)
2. **Get the URLs** using commands above
3. **Test the frontend**: Open `http://<FRONTEND-URL>` in your browser
4. **Test APIs**: Use `http://<AUTH-IP>/api/v1/auth/health` to verify services

## 🔗 Service Endpoints

Once you have the URLs:

- **Frontend**: `http://<FRONTEND-URL>` - Main application
- **Auth API**: `http://<AUTH-IP>/api/v1/auth` - Authentication endpoints
- **Contest API**: `http://<CONTEST-IP>/api/v1/contests` - Contest management

## 📍 Other Services Location

The other services (Submission, Execution, Scoring, Leaderboard) are deployed on **AWS EKS** but are currently **internal only** (ClusterIP). They're accessed through the Frontend, not directly.

**Location**: AWS EKS Cluster (`codeforces-aws-cluster`)

To view them:
```bash
aws eks update-kubeconfig --name codeforces-aws-cluster --region us-east-1
kubectl get services -n codeforces
```

See [SERVICE_LOCATIONS.md](SERVICE_LOCATIONS.md) for complete details.

## ⚠️ Important Notes

- LoadBalancer IPs are **public** - secure your services with authentication
- For production, consider:
  - Setting up Ingress with SSL/TLS
  - Using API Gateway
  - Implementing rate limiting
  - Adding WAF (Web Application Firewall)

