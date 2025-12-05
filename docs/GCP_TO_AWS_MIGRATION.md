# GCP to AWS Migration

## Summary

All GCP resources have been migrated to AWS. The platform now uses a **two-cloud architecture**:

- **AWS**: All compute services (Execution, Submission, Scoring, Leaderboard, Frontend)
- **Azure**: Auth, Contest services, and Database

## Changes Made

### 1. Infrastructure

- ✅ **Removed**: GCP Terraform configuration (`infrastructure/terraform/gcp/`)
- ✅ **Updated**: AWS EKS cluster name from `codeforces-execution-cluster` to `codeforces-aws-cluster`
- ✅ **Updated**: AWS EKS cluster now hosts all AWS services

### 2. Kubernetes Deployments

- ✅ **Updated**: `scoring-service.yaml` - changed `cloud: gcp` → `cloud: aws`
- ✅ **Updated**: `leaderboard-service.yaml` - changed `cloud: gcp` → `cloud: aws`
- ✅ **Updated**: `frontend.yaml` - changed `cloud: gcp` → `cloud: aws`

### 3. CI/CD Pipeline

- ✅ **Removed**: GCP authentication steps
- ✅ **Removed**: GCP Terraform init/plan/apply steps
- ✅ **Removed**: GCP GKE deployment steps
- ✅ **Updated**: AWS EKS cluster name in deployment step

### 4. Documentation

- ✅ **Updated**: README.md - removed GCP from multi-cloud distribution
- ✅ **Updated**: TERRAFORM_SETUP.md - removed GCP setup section

## New Architecture

### Service Distribution

**AWS (EKS Cluster: `codeforces-aws-cluster`):**
- Execution Service
- Submission Service
- Scoring Service
- Leaderboard Service
- Frontend

**Azure (AKS Cluster: `codeforces-aks-cluster`):**
- Auth Service
- Contest Service
- PostgreSQL Database

## GitHub Secrets

You can now **remove** these GCP-related secrets (no longer needed):
- `GCP_PROJECT_ID`
- `GCP_SA_KEY`

**Required secrets** (keep these):
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AZURE_CREDENTIALS`
- `DB_ADMIN_LOGIN`
- `DB_ADMIN_PASSWORD`

## Deployment

The deployment process is now simpler:

1. **Terraform** creates:
   - AWS EKS cluster (all AWS services)
   - Azure AKS cluster (Auth, Contest, Database)

2. **Kubernetes** deploys:
   - All services to their respective clusters

## Benefits

1. **Simplified**: One less cloud provider to manage
2. **Cost**: No GCP billing account needed
3. **Consistency**: All compute services in one place (AWS)
4. **Easier**: Fewer credentials and configurations

## Next Steps

1. **Remove GCP secrets** from GitHub (if you want):
   - Go to Settings → Secrets and variables → Actions
   - Delete `GCP_PROJECT_ID` and `GCP_SA_KEY`

2. **Deploy**:
   ```bash
   git add .
   git commit -m "Migrate all GCP resources to AWS"
   git push origin main
   ```

3. **Verify**:
   - Check AWS EKS cluster is created
   - Verify all services deploy to AWS
   - Check Azure AKS cluster for Auth/Contest services

## Rollback (if needed)

If you need to rollback, you can:
1. Restore GCP Terraform files from git history
2. Restore GCP deployment steps in workflow
3. Revert Kubernetes deployment labels

But this migration is recommended as it simplifies the architecture significantly.

