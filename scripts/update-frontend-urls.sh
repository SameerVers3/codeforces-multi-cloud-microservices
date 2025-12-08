#!/bin/bash
# Script to update ConfigMaps with actual service URLs
# This updates both frontend-config and submission-service-config with Azure LoadBalancer IPs

set -e

echo "=== Updating Service URLs for Multi-Cloud Deployment ==="
echo ""

# Get Azure AKS credentials
echo "Step 1: Connecting to Azure AKS..."
az aks get-credentials --resource-group codeforces-rg --name codeforces-aks-cluster --overwrite-existing

# Wait for LoadBalancers to be provisioned
echo ""
echo "Step 2: Waiting for LoadBalancers to provision (this may take 2-5 minutes)..."
MAX_WAIT=300  # 5 minutes
WAITED=0
while [ $WAITED -lt $MAX_WAIT ]; do
  AUTH_IP=$(kubectl get svc auth-service -n codeforces -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "")
  CONTEST_IP=$(kubectl get svc contest-service -n codeforces -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "")
  
  if [ -n "$AUTH_IP" ] && [ "$AUTH_IP" != "<pending>" ] && [ -n "$CONTEST_IP" ] && [ "$CONTEST_IP" != "<pending>" ]; then
    break
  fi
  
  echo "  Waiting... ($WAITED/$MAX_WAIT seconds)"
  sleep 10
  WAITED=$((WAITED + 10))
done

# Get service IPs
echo ""
echo "Step 3: Getting service external IPs from Azure AKS..."
AUTH_IP=$(kubectl get svc auth-service -n codeforces -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "")
CONTEST_IP=$(kubectl get svc contest-service -n codeforces -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "")

if [ -z "$AUTH_IP" ] || [ "$AUTH_IP" == "<pending>" ]; then
  echo "⚠️  ERROR: Auth service doesn't have an external IP"
  echo "   Make sure auth-service is type LoadBalancer and wait a few minutes"
  echo "   Current status:"
  kubectl get svc auth-service -n codeforces
  exit 1
else
  AUTH_URL="http://${AUTH_IP}"
  echo "✓ Auth service IP: $AUTH_IP"
fi

if [ -z "$CONTEST_IP" ] || [ "$CONTEST_IP" == "<pending>" ]; then
  echo "⚠️  ERROR: Contest service doesn't have an external IP"
  echo "   Make sure contest-service is type LoadBalancer and wait a few minutes"
  echo "   Current status:"
  kubectl get svc contest-service -n codeforces
  exit 1
else
  CONTEST_URL="http://${CONTEST_IP}"
  echo "✓ Contest service IP: $CONTEST_IP"
fi

# Switch to AWS EKS
echo ""
echo "Step 4: Connecting to AWS EKS..."
aws eks update-kubeconfig --name codeforces-aws-cluster --region us-east-1

# Update frontend ConfigMap
echo ""
echo "Step 5: Updating frontend-config ConfigMap..."
kubectl create configmap frontend-config \
  --from-literal=AUTH_SERVICE_URL="$AUTH_URL" \
  --from-literal=CONTEST_SERVICE_URL="$CONTEST_URL" \
  --from-literal=SUBMISSION_SERVICE_URL="http://submission-service.codeforces.svc.cluster.local:80" \
  --from-literal=LEADERBOARD_SERVICE_URL="http://leaderboard-service.codeforces.svc.cluster.local:80" \
  -n codeforces --dry-run=client -o yaml | kubectl apply -f -

# Update submission-service ConfigMap
echo ""
echo "Step 6: Updating submission-service-config ConfigMap..."
kubectl create configmap submission-service-config \
  --from-literal=AUTH_SERVICE_URL="$AUTH_URL" \
  --from-literal=CONTEST_SERVICE_URL="$CONTEST_URL" \
  --from-literal=EXECUTION_SERVICE_URL="http://execution-service.codeforces.svc.cluster.local:80" \
  -n codeforces --dry-run=client -o yaml | kubectl apply -f -

echo ""
echo "✅ ConfigMaps updated successfully!"
echo ""
echo "Step 7: Restarting deployments to pick up new URLs..."
kubectl rollout restart deployment frontend -n codeforces
kubectl rollout restart deployment submission-service -n codeforces

echo ""
echo "✅ Done! Services will restart with new URLs."
echo ""
echo "To verify:"
echo "  kubectl get configmap frontend-config -n codeforces -o yaml"
echo "  kubectl get configmap submission-service-config -n codeforces -o yaml"
echo "  kubectl get pods -n codeforces -l app=frontend"
echo "  kubectl get pods -n codeforces -l app=submission-service"

