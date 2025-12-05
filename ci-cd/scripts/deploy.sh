#!/bin/bash
set -e

# Multi-cloud deployment script
# Usage: ./deploy.sh [aws|azure|gcp|all]

CLOUD=${1:-all}

echo "Starting deployment to: $CLOUD"

# Deploy to AWS
if [ "$CLOUD" = "aws" ] || [ "$CLOUD" = "all" ]; then
    echo "Deploying to AWS..."
    cd infrastructure/terraform/aws
    terraform init
    terraform plan -out=tfplan
    terraform apply tfplan
    
    # Configure kubectl
    aws eks update-kubeconfig --name codeforces-execution-cluster --region us-east-1
    
    # Deploy services
    kubectl apply -f ../../kubernetes/base/
    kubectl apply -f ../../kubernetes/network-policies.yaml
    kubectl apply -f ../../kubernetes/rbac.yaml
fi

# Deploy to Azure
if [ "$CLOUD" = "azure" ] || [ "$CLOUD" = "all" ]; then
    echo "Deploying to Azure..."
    cd infrastructure/terraform/azure
    terraform init
    terraform plan -out=tfplan -var="db_admin_login=$DB_ADMIN_LOGIN" -var="db_admin_password=$DB_ADMIN_PASSWORD"
    terraform apply tfplan
    
    # Configure kubectl
    az aks get-credentials --resource-group codeforces-rg --name codeforces-aks-cluster
    
    # Deploy services
    kubectl apply -f ../../kubernetes/base/
    kubectl apply -f ../../kubernetes/network-policies.yaml
    kubectl apply -f ../../kubernetes/rbac.yaml
fi

# Deploy to GCP
if [ "$CLOUD" = "gcp" ] || [ "$CLOUD" = "all" ]; then
    echo "Deploying to GCP..."
    cd infrastructure/terraform/gcp
    terraform init
    terraform plan -out=tfplan -var="gcp_project_id=$GCP_PROJECT_ID"
    terraform apply tfplan
    
    # Configure kubectl
    gcloud container clusters get-credentials codeforces-gke-cluster --region us-central1
    
    # Deploy services
    kubectl apply -f ../../kubernetes/base/
    kubectl apply -f ../../kubernetes/network-policies.yaml
    kubectl apply -f ../../kubernetes/rbac.yaml
fi

echo "Deployment complete!"

