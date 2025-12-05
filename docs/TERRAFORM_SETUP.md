# Terraform Setup Guide

## Prerequisites

Before deploying infrastructure, you need to set up authentication for each cloud provider:

### AWS Setup

1. **Install AWS CLI**:
   ```bash
   curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
   unzip awscliv2.zip
   sudo ./aws/install
   ```

2. **Configure AWS Credentials**:
   ```bash
   aws configure
   # Enter your AWS Access Key ID
   # Enter your AWS Secret Access Key
   # Enter default region (e.g., us-east-1)
   # Enter default output format (json)
   ```

3. **Set GitHub Secrets**:
   - `AWS_ACCESS_KEY_ID`: Your AWS access key
   - `AWS_SECRET_ACCESS_KEY`: Your AWS secret key

   **Note**: These secrets are required for the CI/CD pipeline to deploy to AWS.

### Azure Setup

1. **Install Azure CLI**:
   ```bash
   curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
   ```

2. **Login to Azure**:
   ```bash
   az login
   ```

3. **Create Service Principal**:
   ```bash
   az ad sp create-for-rbac --name "codeforces-terraform" \
     --role contributor \
     --scopes /subscriptions/{subscription-id} \
     --sdk-auth
   ```

4. **Set GitHub Secrets**:
   - `AZURE_CLIENT_ID`: From service principal output
   - `AZURE_CLIENT_SECRET`: From service principal output
   - `AZURE_TENANT_ID`: From service principal output
   - `AZURE_CREDENTIALS`: JSON output from `az ad sp create-for-rbac --sdk-auth` (alternative to individual secrets)
   - `DB_ADMIN_LOGIN`: Database admin username
   - `DB_ADMIN_PASSWORD`: Database admin password

   **Note**: You can use either individual secrets (`AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID`) or the `AZURE_CREDENTIALS` JSON secret.

### GCP Setup

1. **Install Google Cloud SDK**:
   ```bash
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL
   gcloud init
   ```

2. **Create Service Account**:
   ```bash
   gcloud iam service-accounts create terraform-sa \
     --display-name="Terraform Service Account"
   
   gcloud projects add-iam-policy-binding PROJECT_ID \
     --member="serviceAccount:terraform-sa@PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/editor"
   
   gcloud iam service-accounts keys create key.json \
     --iam-account=terraform-sa@PROJECT_ID.iam.gserviceaccount.com
   ```

3. **Set GitHub Secrets**:
   - `GCP_PROJECT_ID`: Your GCP project ID
   - `GCP_SA_KEY`: Base64 encoded service account JSON key
     ```bash
     cat key.json | base64 -w 0
     ```

## Local Development

### Initialize Terraform

```bash
# AWS
cd infrastructure/terraform/aws
terraform init

# Azure
cd infrastructure/terraform/azure
terraform init

# GCP
cd infrastructure/terraform/gcp
terraform init
```

### Plan Changes

```bash
# AWS
cd infrastructure/terraform/aws
terraform plan

# Azure
cd infrastructure/terraform/azure
terraform plan -var="db_admin_login=your_admin" -var="db_admin_password=your_password"

# GCP
cd infrastructure/terraform/gcp
terraform plan -var="gcp_project_id=your-project-id"
```

### Apply Changes

```bash
# AWS
cd infrastructure/terraform/aws
terraform apply

# Azure
cd infrastructure/terraform/azure
terraform apply -var="db_admin_login=your_admin" -var="db_admin_password=your_password"

# GCP
cd infrastructure/terraform/gcp
terraform apply -var="gcp_project_id=your-project-id"
```

## CI/CD Deployment

The GitHub Actions workflow automatically:

1. **Initializes Terraform** for all three providers
2. **Plans changes** (shows what will be created/modified)
3. **Applies changes** (only on `main` branch)

### Required GitHub Secrets

Make sure these are set in your repository settings:

**AWS:**
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

**Azure:**
- `AZURE_CLIENT_ID`
- `AZURE_CLIENT_SECRET`
- `AZURE_TENANT_ID`
- `DB_ADMIN_LOGIN`
- `DB_ADMIN_PASSWORD`

**GCP:**
- `GCP_PROJECT_ID`
- `GCP_SA_KEY` (base64 encoded JSON)

## Troubleshooting

### Terraform Init Errors

**Error**: `Duplicate variable/output definition`

**Solution**: Variables and outputs should only be defined in `variables.tf` and `outputs.tf` files, not in `main.tf`. Remove duplicates from `main.tf`.

### Authentication Errors

**Error**: `No valid credential sources found`

**Solution**: 
- Ensure GitHub Secrets are set correctly
- For local development, configure credentials using cloud provider CLIs
- Check that service accounts have necessary permissions

### Resource Creation Failures

**Error**: `Error creating resource`

**Solution**:
- Check cloud provider quotas/limits
- Verify service account permissions
- Review cloud provider console for detailed error messages

## Cost Estimation

Before deploying, estimate costs:

- **AWS EKS**: ~$73/month (cluster) + node costs
- **Azure AKS**: ~$73/month (cluster) + node costs
- **GCP GKE**: ~$73/month (cluster) + node costs
- **PostgreSQL**: ~$50-200/month depending on tier
- **Load Balancers**: ~$20-50/month each

**Total estimated monthly cost**: $300-600+ depending on usage

## Cleanup

To destroy all infrastructure:

```bash
# AWS
cd infrastructure/terraform/aws
terraform destroy

# Azure
cd infrastructure/terraform/azure
terraform destroy -var="db_admin_login=your_admin" -var="db_admin_password=your_password"

# GCP
cd infrastructure/terraform/gcp
terraform destroy -var="gcp_project_id=your-project-id"
```

**Warning**: This will delete all resources. Make sure you have backups!

