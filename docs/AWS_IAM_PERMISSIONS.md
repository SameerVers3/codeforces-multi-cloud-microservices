# AWS IAM Permissions Guide

## Required IAM Permissions for Terraform Deployment

To deploy the Codeforces platform infrastructure to AWS, your IAM user/service account needs specific permissions. This guide outlines the minimum required permissions.

## Quick Start (Recommended)

### Option A: Use PowerUserAccess (Development/Testing)

**Fastest way to get started:**

```bash
# Create IAM user
aws iam create-user --user-name codeforces-terraform

# Attach PowerUserAccess policy
aws iam attach-user-policy \
  --user-name codeforces-terraform \
  --policy-arn arn:aws:iam::aws:policy/PowerUserAccess

# Create access keys
aws iam create-access-key --user-name codeforces-terraform
```

**Note**: PowerUserAccess provides full access except IAM user/group management. Good for development, but use Option B for production.

### Option B: Use Custom Policy (Production)

**Use the provided IAM policy file:**

```bash
# Create IAM user
aws iam create-user --user-name codeforces-terraform

# Create policy from file and capture the ARN
POLICY_ARN=$(aws iam create-policy \
  --policy-name CodeforcesTerraformPolicy \
  --policy-document file://infrastructure/terraform/aws/iam-policy.json \
  --query 'Policy.Arn' --output text)

# Attach policy to user using the captured ARN
aws iam attach-user-policy \
  --user-name codeforces-terraform \
  --policy-arn $POLICY_ARN

# Create access keys
aws iam create-access-key --user-name codeforces-terraform
```

**Save the AccessKeyId and SecretAccessKey** - you'll need these for GitHub Secrets!

**Alternative (if you know your AWS Account ID):**

```bash
# Create IAM user
aws iam create-user --user-name codeforces-terraform

# Create policy from file
aws iam create-policy \
  --policy-name CodeforcesTerraformPolicy \
  --policy-document file://infrastructure/terraform/aws/iam-policy.json

# Attach policy to user (replace YOUR_ACCOUNT_ID with your AWS account ID)
aws iam attach-user-policy \
  --user-name codeforces-terraform \
  --policy-arn arn:aws:iam::YOUR_ACCOUNT_ID:policy/CodeforcesTerraformPolicy

# Create access keys
aws iam create-access-key --user-name codeforces-terraform
```

## Option 1: AWS Managed Policies (Recommended for Quick Setup)

### For Terraform Deployment

Attach these AWS managed policies to your IAM user:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "eks:*",
        "ec2:*",
        "iam:*",
        "elasticloadbalancing:*",
        "autoscaling:*",
        "cloudformation:*",
        "logs:*",
        "route53:*",
        "acm:*"
      ],
      "Resource": "*"
    }
  ]
}
```

**Note**: This is very permissive. For production, use Option 2 with specific permissions.

### AWS Managed Policies You Can Use

1. **PowerUserAccess** (for development/testing)
   - Provides full access except IAM user/group management
   - Not recommended for production

2. **AmazonEKSClusterPolicy** (for EKS)
   - Already included in EKS service role

3. **AmazonEC2FullAccess** (for VPC, subnets, etc.)
   - Provides EC2 and VPC management

4. **ElasticLoadBalancingFullAccess** (for ALB)
   - Provides load balancer management

## Option 2: Custom IAM Policy (Recommended for Production)

Create a custom IAM policy with minimal required permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EKSClusterManagement",
      "Effect": "Allow",
      "Action": [
        "eks:CreateCluster",
        "eks:DescribeCluster",
        "eks:UpdateCluster",
        "eks:DeleteCluster",
        "eks:ListClusters",
        "eks:UpdateClusterVersion",
        "eks:UpdateClusterConfig",
        "eks:TagResource",
        "eks:UntagResource"
      ],
      "Resource": "arn:aws:eks:*:*:cluster/codeforces-execution-cluster"
    },
    {
      "Sid": "EC2VPCManagement",
      "Effect": "Allow",
      "Action": [
        "ec2:CreateVpc",
        "ec2:DescribeVpcs",
        "ec2:ModifyVpcAttribute",
        "ec2:DeleteVpc",
        "ec2:CreateSubnet",
        "ec2:DescribeSubnets",
        "ec2:ModifySubnetAttribute",
        "ec2:DeleteSubnet",
        "ec2:CreateInternetGateway",
        "ec2:DescribeInternetGateways",
        "ec2:AttachInternetGateway",
        "ec2:DetachInternetGateway",
        "ec2:DeleteInternetGateway",
        "ec2:CreateRouteTable",
        "ec2:DescribeRouteTables",
        "ec2:CreateRoute",
        "ec2:DeleteRoute",
        "ec2:DeleteRouteTable",
        "ec2:AssociateRouteTable",
        "ec2:DisassociateRouteTable",
        "ec2:DescribeAvailabilityZones",
        "ec2:DescribeAccountAttributes",
        "ec2:AllocateAddress",
        "ec2:ReleaseAddress",
        "ec2:DescribeAddresses",
        "ec2:CreateSecurityGroup",
        "ec2:DescribeSecurityGroups",
        "ec2:AuthorizeSecurityGroupIngress",
        "ec2:AuthorizeSecurityGroupEgress",
        "ec2:RevokeSecurityGroupIngress",
        "ec2:RevokeSecurityGroupEgress",
        "ec2:DeleteSecurityGroup",
        "ec2:CreateTags",
        "ec2:DescribeTags",
        "ec2:DeleteTags"
      ],
      "Resource": "*"
    },
    {
      "Sid": "LoadBalancerManagement",
      "Effect": "Allow",
      "Action": [
        "elasticloadbalancing:CreateLoadBalancer",
        "elasticloadbalancing:DescribeLoadBalancers",
        "elasticloadbalancing:ModifyLoadBalancerAttributes",
        "elasticloadbalancing:DeleteLoadBalancer",
        "elasticloadbalancing:CreateTargetGroup",
        "elasticloadbalancing:DescribeTargetGroups",
        "elasticloadbalancing:ModifyTargetGroup",
        "elasticloadbalancing:DeleteTargetGroup",
        "elasticloadbalancing:RegisterTargets",
        "elasticloadbalancing:DeregisterTargets",
        "elasticloadbalancing:CreateListener",
        "elasticloadbalancing:DescribeListeners",
        "elasticloadbalancing:ModifyListener",
        "elasticloadbalancing:DeleteListener",
        "elasticloadbalancing:AddTags",
        "elasticloadbalancing:RemoveTags",
        "elasticloadbalancing:DescribeTags"
      ],
      "Resource": "*"
    },
    {
      "Sid": "IAMRoleManagement",
      "Effect": "Allow",
      "Action": [
        "iam:CreateRole",
        "iam:GetRole",
        "iam:UpdateRole",
        "iam:DeleteRole",
        "iam:AttachRolePolicy",
        "iam:DetachRolePolicy",
        "iam:ListAttachedRolePolicies",
        "iam:GetRolePolicy",
        "iam:PutRolePolicy",
        "iam:DeleteRolePolicy",
        "iam:ListRolePolicies",
        "iam:TagRole",
        "iam:UntagRole",
        "iam:PassRole",
        "iam:CreateServiceLinkedRole"
      ],
      "Resource": [
        "arn:aws:iam::*:role/codeforces-eks-cluster-role",
        "arn:aws:iam::*:role/codeforces-eks-node-role",
        "arn:aws:iam::*:role/aws-service-role/eks.amazonaws.com/AWSServiceRoleForAmazonEKS"
      ]
    },
    {
      "Sid": "CloudFormationManagement",
      "Effect": "Allow",
      "Action": [
        "cloudformation:CreateStack",
        "cloudformation:DescribeStacks",
        "cloudformation:UpdateStack",
        "cloudformation:DeleteStack",
        "cloudformation:DescribeStackEvents",
        "cloudformation:DescribeStackResources",
        "cloudformation:GetTemplate",
        "cloudformation:ValidateTemplate"
      ],
      "Resource": "*"
    },
    {
      "Sid": "LogsManagement",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:DescribeLogGroups",
        "logs:DeleteLogGroup",
        "logs:PutRetentionPolicy"
      ],
      "Resource": "arn:aws:logs:*:*:log-group:/aws/eks/codeforces-execution-cluster/*"
    },
    {
      "Sid": "AutoScalingManagement",
      "Effect": "Allow",
      "Action": [
        "autoscaling:CreateAutoScalingGroup",
        "autoscaling:DescribeAutoScalingGroups",
        "autoscaling:UpdateAutoScalingGroup",
        "autoscaling:DeleteAutoScalingGroup",
        "autoscaling:CreateLaunchConfiguration",
        "autoscaling:DescribeLaunchConfigurations",
        "autoscaling:DeleteLaunchConfiguration",
        "autoscaling:AttachInstances",
        "autoscaling:DetachInstances",
        "autoscaling:SetDesiredCapacity",
        "autoscaling:EnableMetricsCollection",
        "autoscaling:DisableMetricsCollection"
      ],
      "Resource": "*"
    }
  ]
}
```

## Option 3: Service Account with Specific Permissions

For CI/CD pipelines, create a dedicated IAM user with:

### Minimum Required Permissions

1. **EKS Cluster Management**
   - `eks:*` on cluster resources

2. **VPC and Networking**
   - `ec2:CreateVpc`, `ec2:DescribeVpcs`, `ec2:DeleteVpc`
   - `ec2:CreateSubnet`, `ec2:DescribeSubnets`, `ec2:DeleteSubnet`
   - `ec2:CreateInternetGateway`, `ec2:AttachInternetGateway`
   - `ec2:CreateRouteTable`, `ec2:CreateRoute`
   - `ec2:CreateSecurityGroup`, `ec2:AuthorizeSecurityGroupIngress`

3. **Load Balancer**
   - `elasticloadbalancing:*`

4. **IAM Roles** (for EKS service roles)
   - `iam:CreateRole`, `iam:AttachRolePolicy`, `iam:PassRole`

5. **CloudFormation** (used by EKS)
   - `cloudformation:*`

6. **Logs** (for EKS cluster logs)
   - `logs:CreateLogGroup`, `logs:PutRetentionPolicy`

## Step-by-Step Setup

### 1. Create IAM User

```bash
aws iam create-user --user-name codeforces-terraform
```

### 2. Create Access Keys

```bash
aws iam create-access-key --user-name codeforces-terraform
```

Save the `AccessKeyId` and `SecretAccessKey` - you'll need these for GitHub Secrets.

### 3. Attach Policy

**Option A: Attach Custom Policy**

```bash
# Create the policy file
cat > codeforces-terraform-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "eks:*",
        "ec2:*",
        "iam:CreateRole",
        "iam:AttachRolePolicy",
        "iam:PassRole",
        "iam:GetRole",
        "iam:ListAttachedRolePolicies",
        "elasticloadbalancing:*",
        "autoscaling:*",
        "cloudformation:*",
        "logs:CreateLogGroup",
        "logs:PutRetentionPolicy"
      ],
      "Resource": "*"
    }
  ]
}
EOF

# Create the policy
aws iam create-policy \
  --policy-name CodeforcesTerraformPolicy \
  --policy-document file://codeforces-terraform-policy.json

# Attach to user
aws iam attach-user-policy \
  --user-name codeforces-terraform \
  --policy-arn arn:aws:iam::YOUR_ACCOUNT_ID:policy/CodeforcesTerraformPolicy
```

**Option B: Use PowerUserAccess (Development Only)**

```bash
aws iam attach-user-policy \
  --user-name codeforces-terraform \
  --policy-arn arn:aws:iam::aws:policy/PowerUserAccess
```

### 4. Set Up GitHub Secrets

Add these secrets to your GitHub repository:

- `AWS_ACCESS_KEY_ID`: From step 2
- `AWS_SECRET_ACCESS_KEY`: From step 2

## Additional Permissions for Kubernetes Operations

If you need to deploy/manage Kubernetes resources directly (not just via Terraform), add:

```json
{
  "Effect": "Allow",
  "Action": [
    "eks:DescribeCluster",
    "eks:ListClusters",
    "eks:AccessKubernetesApi",
    "eks:DescribeUpdate",
    "eks:ListUpdates"
  ],
  "Resource": "*"
}
```

## Security Best Practices

1. **Use Least Privilege**: Start with minimal permissions and add as needed
2. **Use IAM Roles**: For EC2/ECS instances, use IAM roles instead of access keys
3. **Rotate Credentials**: Regularly rotate access keys
4. **Enable MFA**: Enable Multi-Factor Authentication for IAM users
5. **Use Separate Accounts**: Use different IAM users for different environments
6. **Monitor Access**: Enable CloudTrail to audit IAM actions

## Troubleshooting

### Error: "User is not authorized to perform: eks:CreateCluster"

**Solution**: Ensure the IAM user has `eks:*` permissions and `iam:PassRole` permission for the EKS service role.

### Error: "Unable to assume IAM role"

**Solution**: Ensure `iam:PassRole` permission is granted for the EKS cluster role ARN.

### Error: "Cannot create VPC"

**Solution**: Ensure `ec2:*` permissions or at least `ec2:CreateVpc`, `ec2:CreateSubnet`, etc.

## Quick Reference

### Minimum Permissions Summary

- **EKS**: `eks:*`
- **EC2/VPC**: `ec2:*` (or specific VPC/subnet/security group actions)
- **IAM**: `iam:CreateRole`, `iam:AttachRolePolicy`, `iam:PassRole`
- **Load Balancer**: `elasticloadbalancing:*`
- **CloudFormation**: `cloudformation:*`
- **Logs**: `logs:CreateLogGroup`, `logs:PutRetentionPolicy`
- **Auto Scaling**: `autoscaling:*`

### Testing Permissions

```bash
# Test EKS permissions
aws eks list-clusters

# Test EC2 permissions
aws ec2 describe-vpcs

# Test IAM permissions
aws iam get-user
```

## Production Recommendations

For production environments:

1. **Use IAM Roles**: Instead of access keys, use IAM roles for EC2/GitHub Actions
2. **Scoped Policies**: Create policies scoped to specific resources (not `*`)
3. **Resource Tags**: Use resource tags to restrict access
4. **Separate Accounts**: Use separate AWS accounts for dev/staging/prod
5. **CloudTrail**: Enable CloudTrail for audit logging
6. **AWS Organizations**: Use AWS Organizations for multi-account management

