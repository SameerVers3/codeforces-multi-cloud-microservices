# Deployment Guide

## Prerequisites

Before deploying, ensure you have:

1. **GitHub Repository**: Your code pushed to GitHub
2. **GitHub Secrets Configured**:
   - `GITHUB_TOKEN` (automatically provided)
   - `AWS_ACCESS_KEY_ID` (for AWS deployment)
   - `AWS_SECRET_ACCESS_KEY` (for AWS deployment)
   - `AZURE_CREDENTIALS` (JSON with clientId, clientSecret, subscriptionId, tenantId)
   - `DB_ADMIN_LOGIN` (Database admin username)
   - `DB_ADMIN_PASSWORD` (Database admin password)

3. **Cloud Provider Accounts**:
   - AWS account with appropriate permissions
   - Azure subscription

## GitHub Secrets Setup

### Setting up GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret listed above

### AWS Credentials

```bash
# Get AWS credentials from AWS IAM Console
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
```

### Azure Credentials

```bash
# Create a service principal in Azure
az ad sp create-for-rbac --name "codeforces-sp" --role contributor \
  --scopes /subscriptions/{subscription-id} \
  --sdk-auth

# This outputs JSON with clientId, clientSecret, subscriptionId, tenantId
```


## Deployment Steps

### 1. Local Testing

Before deploying to production, test locally:

```bash
# Start all services locally
docker-compose up -d

# Run tests
cd services/auth-service
pytest tests/ -v

# Check health endpoints
curl http://localhost:8001/health
```

### 2. Push to GitHub

The CI/CD pipeline automatically triggers on push to `main` or `develop` branches:

```bash
git add .
git commit -m "Deploy to production"
git push origin main
```

### 3. Monitor GitHub Actions

1. Go to your GitHub repository
2. Click on **Actions** tab
3. Watch the workflow run:
   - **Build**: Builds Docker images for all services
   - **Test**: Runs unit tests
   - **Deploy**: Deploys to cloud providers (only on `main` branch)

### 4. Verify Deployment

After deployment completes:

#### AWS (Execution & Submission Services)
```bash
# Get EKS cluster credentials
aws eks update-kubeconfig --name codeforces-aws-cluster --region us-east-1

# Check pods
kubectl get pods -n codeforces

# Check services
kubectl get services -n codeforces
```

#### Azure (Auth & Contest Services)
```bash
# Get AKS cluster credentials
az aks get-credentials --resource-group codeforces-rg --name codeforces-aks-cluster

# Check pods
kubectl get pods -n codeforces

# Check services
kubectl get services -n codeforces
```

#### GCP (Scoring & Leaderboard Services)
```bash
# Get GKE cluster credentials
gcloud container clusters get-credentials codeforces-gke-cluster --region us-central1

# Check pods
kubectl get pods -n codeforces

# Check services
kubectl get services -n codeforces
```

## Troubleshooting

### Docker Build Failures

**Error**: `repository name must be lowercase`

**Solution**: The workflow now converts repository names to lowercase automatically. Ensure your GitHub repository name doesn't contain uppercase letters, or use the `IMAGE_PREFIX` override.

### CodeQL Action Deprecation

**Error**: `CodeQL Action major versions v1 and v2 have been deprecated`

**Solution**: Updated to v3 in the workflow file.

### Trivy Results Not Found

**Error**: `Path does not exist: trivy-results.sarif`

**Solution**: The workflow now only uploads Trivy results if the scan succeeds and the file exists. This is handled with conditional checks.

### Terraform Authentication Errors

**Error**: `Error: No valid credential sources found`

**Solution**: Ensure all cloud provider credentials are set in GitHub Secrets:
- AWS: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
- Azure: `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID`
- GCP: `GCP_SA_KEY` (base64 encoded JSON)

### Kubernetes Deployment Failures

**Error**: `Error from server (Forbidden)`

**Solution**: Ensure RBAC is properly configured and the service account has necessary permissions.

## Manual Deployment

If you need to deploy manually:

### 1. Build Docker Images

```bash
# Build all services
for service in auth-service contest-service submission-service execution-service scoring-service leaderboard-service; do
  docker build -t ghcr.io/$GITHUB_USER/codeforces-multi-cloud-microservices/$service:latest ./services/$service
done

# Build frontend
docker build -t ghcr.io/$GITHUB_USER/codeforces-multi-cloud-microservices/frontend:latest ./frontend/nextjs-app
```

### 2. Push to Registry

```bash
# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u $GITHUB_USER --password-stdin

# Push images
docker push ghcr.io/$GITHUB_USER/codeforces-multi-cloud-microservices/auth-service:latest
# ... repeat for all services
```

### 3. Deploy with Terraform

```bash
# AWS
cd infrastructure/terraform/aws
terraform init
terraform plan
terraform apply

# Azure
cd infrastructure/terraform/azure
terraform init
terraform plan -var="db_admin_login=$DB_ADMIN_LOGIN" -var="db_admin_password=$DB_ADMIN_PASSWORD"
terraform apply -var="db_admin_login=$DB_ADMIN_LOGIN" -var="db_admin_password=$DB_ADMIN_PASSWORD"

# GCP
cd infrastructure/terraform/gcp
terraform init
terraform plan -var="gcp_project_id=$GCP_PROJECT_ID"
terraform apply -var="gcp_project_id=$GCP_PROJECT_ID"
```

### 4. Deploy to Kubernetes

```bash
# Apply Kubernetes manifests
kubectl apply -f infrastructure/kubernetes/base/
kubectl apply -f infrastructure/kubernetes/network-policies.yaml
kubectl apply -f infrastructure/kubernetes/rbac.yaml
```

## Post-Deployment

1. **Verify Health Checks**:
   ```bash
   curl https://your-domain.com/health
   ```

2. **Check Logs**:
   ```bash
   kubectl logs -n codeforces -l app=auth-service
   ```

3. **Monitor Metrics**:
   - Access Grafana dashboards
   - Check Prometheus metrics
   - Review application logs

4. **Test Endpoints**:
   ```bash
   # Test authentication
   curl -X POST https://api.your-domain.com/api/v1/auth/register \
     -H "Content-Type: application/json" \
     -d '{"username":"test","email":"test@example.com","password":"test123"}'
   ```

## Rollback

To rollback to a previous version:

```bash
# Get previous image tag
PREVIOUS_SHA=<previous-commit-sha>

# Update Kubernetes deployments
kubectl set image deployment/auth-service \
  auth-service=ghcr.io/$GITHUB_USER/codeforces-multi-cloud-microservices/auth-service:$PREVIOUS_SHA \
  -n codeforces

# Repeat for all services
```

## Continuous Deployment

The workflow is configured for:
- **Automatic builds** on every push to `main` or `develop`
- **Automatic tests** on every pull request
- **Automatic deployment** only on push to `main` branch

To disable automatic deployment, remove or comment out the `deploy` job in `.github/workflows/deploy.yml`.

