# Service Deployment Locations

## Multi-Cloud Architecture

### AWS EKS Cluster (`codeforces-aws-cluster`)
Located in: `us-east-1`

| Service | Type | Status | Access |
|---------|------|--------|--------|
| **Frontend** | LoadBalancer | ✅ Exposed | External URL |
| **Submission Service** | ClusterIP | 🔒 Internal | Via Frontend |
| **Execution Service** | ClusterIP | 🔒 Internal | Via Frontend |
| **Scoring Service** | ClusterIP | 🔒 Internal | Via Frontend |
| **Leaderboard Service** | ClusterIP | 🔒 Internal | Via Frontend |

### Azure AKS Cluster (`codeforces-aks-cluster`)
Located in: `eastus`

| Service | Type | Status | Access |
|---------|------|--------|--------|
| **Auth Service** | LoadBalancer | ✅ Exposed | External IP |
| **Contest Service** | LoadBalancer | ✅ Exposed | External IP |

## Current Architecture

```
Internet
   │
   ├─→ Frontend (AWS LoadBalancer) ──→ Auth Service (Azure LoadBalancer)
   │                                    Contest Service (Azure LoadBalancer)
   │
   └─→ Internal Services (AWS ClusterIP):
       ├─ Submission Service
       ├─ Execution Service
       ├─ Scoring Service
       └─ Leaderboard Service
```

## Why Some Services Are Internal?

The backend services (Submission, Execution, Scoring, Leaderboard) are currently `ClusterIP` because:

1. **Security**: They don't need direct internet access
2. **Architecture**: They're called by the Frontend, not directly by users
3. **Cost**: Fewer LoadBalancers = lower cost
4. **Best Practice**: Only expose what's necessary

## Accessing Internal Services

### Option 1: Via Frontend (Recommended)
All user interactions go through the Frontend, which internally calls these services.

### Option 2: Port Forwarding (For Testing)
```bash
# Connect to AWS EKS
aws eks update-kubeconfig --name codeforces-aws-cluster --region us-east-1

# Port forward to services
kubectl port-forward -n codeforces service/submission-service 8003:80
kubectl port-forward -n codeforces service/execution-service 8004:80
kubectl port-forward -n codeforces service/scoring-service 8005:80
kubectl port-forward -n codeforces service/leaderboard-service 8006:80
```

Then access:
- Submission: `http://localhost:8003`
- Execution: `http://localhost:8004`
- Scoring: `http://localhost:8005`
- Leaderboard: `http://localhost:8006`

### Option 3: Expose as LoadBalancer (If Needed)
If you need direct external access to these services, we can change them to `LoadBalancer`.

## View All Services

### AWS EKS
```bash
aws eks update-kubeconfig --name codeforces-aws-cluster --region us-east-1
kubectl get services -n codeforces
```

### Azure AKS
```bash
az aks get-credentials --resource-group codeforces-rg --name codeforces-aks-cluster
kubectl get services -n codeforces
```

## Service Communication Flow

```
User → Frontend (AWS) → Auth Service (Azure) [for login]
                      → Contest Service (Azure) [for contests]
                      → Submission Service (AWS) [for code submission]
                           └─→ Execution Service (AWS) [executes code]
                           └─→ Scoring Service (AWS) [calculates score]
                           └─→ Leaderboard Service (AWS) [updates leaderboard]
```

## Need to Expose More Services?

If you need direct external access to Submission, Execution, Scoring, or Leaderboard services, I can change them to `LoadBalancer`. However, this is typically not recommended for production unless you have a specific use case.

