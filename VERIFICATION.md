# Deployment Verification Checklist

## ✅ All Critical Issues Fixed

### Infrastructure
- ✅ GCP completely removed
- ✅ AWS EKS cluster name: `codeforces-aws-cluster`
- ✅ Azure AKS cluster name: `codeforces-aks-cluster`
- ✅ Azure PostgreSQL: Flexible Server (not deprecated Single Server)
- ✅ Azure VM size: `standard_dc2s_v3` (available in subscription)
- ✅ AWS IAM permissions: All required permissions included

### Kubernetes
- ✅ All services use `codeforces` namespace (consistent)
- ✅ RBAC uses `codeforces` namespace
- ✅ Network policies use `codeforces` namespace
- ✅ Secrets template uses `codeforces` namespace
- ✅ All AWS services (Execution, Submission, Scoring, Leaderboard, Frontend) labeled `cloud: aws`
- ✅ All Azure services (Auth, Contest) labeled `cloud: azure`
- ✅ Removed obsolete `deployment.yaml` file

### CI/CD Pipeline
- ✅ No GCP references in workflow
- ✅ Docker images tagged with both SHA and `latest`
- ✅ Terraform init only for AWS and Azure
- ✅ Kubernetes deployments use `--validate=false` (safe, clusters don't exist yet)

### Scripts
- ✅ Deploy script updated (no GCP)
- ✅ AWS cluster name updated in deploy script

### Documentation
- ✅ README updated (no GCP)
- ✅ TERRAFORM_SETUP.md updated (no GCP)
- ✅ DEPLOYMENT_GUIDE.md updated (no GCP)
- ✅ All cluster names consistent

## Pre-Deployment Verification

Run these checks before deploying:

```bash
# 1. Verify no GCP references
grep -r "gcp\|GCP\|google\|Google" .github/workflows/ infrastructure/kubernetes/base/ --exclude-dir=node_modules || echo "No GCP references found"

# 2. Verify cluster names are correct
grep -r "codeforces-execution-cluster" . --exclude-dir=node_modules --exclude-dir=.git || echo "No old cluster name found"

# 3. Verify namespace consistency
grep -r "namespace: default" infrastructure/kubernetes/rbac.yaml infrastructure/kubernetes/network-policies.yaml || echo "All use codeforces namespace"

# 4. Check Terraform files exist
ls infrastructure/terraform/aws/main.tf infrastructure/terraform/azure/main.tf && echo "Terraform files exist"
```

## Deployment Test

After pushing, verify:

1. **Build Job**: All services build successfully
2. **Test Job**: All tests pass
3. **Deploy Job**:
   - Terraform init succeeds (no GCP errors)
   - Terraform plan shows resources to create
   - Terraform apply creates infrastructure
   - Kubernetes deployments succeed (after clusters exist)

## Expected Results

### AWS
- VPC created
- EKS cluster `codeforces-aws-cluster` created
- Load balancer created (if ELB enabled)
- All 5 services deployed to EKS

### Azure
- Resource group created
- AKS cluster `codeforces-aks-cluster` created
- PostgreSQL Flexible Server created
- Load balancer created
- 2 services deployed to AKS

## If Something Fails

1. **Check workflow logs** for specific errors
2. **Verify secrets** are set correctly
3. **Check cloud provider quotas** (especially Azure VM sizes)
4. **Verify IAM permissions** (AWS)
5. **Check service principal** permissions (Azure)

## Success Indicators

✅ All jobs complete without errors
✅ Terraform shows "Apply complete!"
✅ Kubernetes pods are running: `kubectl get pods -n codeforces`
✅ Services respond to health checks

