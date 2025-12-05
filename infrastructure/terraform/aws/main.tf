terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Data source for existing VPC (if importing)
# Try to find VPC by tags or use existing EKS cluster's VPC
data "aws_vpc" "existing" {
  count   = var.import_existing_vpc ? 1 : 0
  filter {
    name   = "tag:Name"
    values = ["codeforces-aws-vpc"]
  }
}

# VPC for AWS resources
# If VPC already exists, set import_existing_vpc = true
resource "aws_vpc" "main" {
  count                = var.import_existing_vpc ? 0 : 1
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "codeforces-aws-vpc"
  }
}

# Use existing VPC or created VPC
locals {
  vpc_id = var.import_existing_vpc ? data.aws_vpc.existing[0].id : aws_vpc.main[0].id
}

# Data source for existing EKS cluster (if importing)
data "aws_eks_cluster" "existing" {
  count = var.import_existing_eks_cluster ? 1 : 0
  name  = "codeforces-aws-cluster"
}

# EKS Cluster for all AWS services (Execution, Submission, Scoring, Leaderboard, Frontend)
# If cluster already exists, set import_existing_eks_cluster = true
resource "aws_eks_cluster" "main" {
  count    = var.import_existing_eks_cluster ? 0 : 1
  name     = "codeforces-aws-cluster"
  role_arn = local.eks_cluster_role_arn
  version  = "1.28"

  vpc_config {
    subnet_ids = local.subnet_ids
  }

  # Dependencies are handled automatically through role_arn reference
}

# Data source for existing IAM role (if importing)
data "aws_iam_role" "existing_eks_cluster" {
  count = var.import_existing_iam_role ? 1 : 0
  name  = "codeforces-eks-cluster-role"
}

# IAM Role for EKS Cluster
# If role already exists, set import_existing_iam_role = true
resource "aws_iam_role" "eks_cluster" {
  count = var.import_existing_iam_role ? 0 : 1
  name  = "codeforces-eks-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "eks.amazonaws.com"
      }
    }]
  })

  tags = {
    ManagedBy = "Terraform"
  }
}

# Use existing role or created role
locals {
  eks_cluster_role_arn = var.import_existing_iam_role ? data.aws_iam_role.existing_eks_cluster[0].arn : aws_iam_role.eks_cluster[0].arn
}

resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
  count      = var.import_existing_iam_role ? 0 : 1
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks_cluster[0].name
}

# Subnets
# If VPC already exists, try to use existing subnets or create new ones
resource "aws_subnet" "main" {
  count             = var.import_existing_vpc ? 0 : 2
  vpc_id            = local.vpc_id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "codeforces-subnet-${count.index + 1}"
  }
}

data "aws_availability_zones" "available" {
  state = "available"
}

# Data source for existing Internet Gateway (if importing)
data "aws_internet_gateway" "existing" {
  count = var.import_existing_vpc ? 1 : 0
  filter {
    name   = "attachment.vpc-id"
    values = [local.vpc_id]
  }
}

# Internet Gateway
# If VPC already exists, use existing IGW
resource "aws_internet_gateway" "main" {
  count  = var.import_existing_vpc ? 0 : 1
  vpc_id = aws_vpc.main[0].id

  tags = {
    Name = "codeforces-igw"
  }
}

# Use existing IGW or created IGW
locals {
  igw_id = var.import_existing_vpc ? data.aws_internet_gateway.existing[0].id : aws_internet_gateway.main[0].id
}

# Route Table
resource "aws_route_table" "main" {
  vpc_id = local.vpc_id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = local.igw_id
  }

  tags = {
    Name = "codeforces-rt"
  }
}

resource "aws_route_table_association" "main" {
  count          = length(local.subnet_ids)
  subnet_id      = local.subnet_ids[count.index]
  route_table_id = aws_route_table.main.id
}

# Application Load Balancer
# Note: If your AWS account doesn't have ELB enabled, comment out this resource
# or contact AWS Support to enable ELB service
resource "aws_lb" "main" {
  count              = var.enable_load_balancer ? 1 : 0
  name               = "codeforces-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb[0].id]
  subnets            = aws_subnet.main[*].id

  enable_deletion_protection = false
}

resource "aws_security_group" "alb" {
  count       = var.enable_load_balancer ? 1 : 0
  name_prefix = "codeforces-alb-"
  vpc_id      = local.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

