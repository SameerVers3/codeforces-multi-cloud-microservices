variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
  default     = "codeforces-aws-cluster"
}

variable "node_instance_type" {
  description = "EC2 instance type for EKS nodes"
  type        = string
  default     = "t3.medium"
}

variable "node_count" {
  description = "Number of EKS nodes"
  type        = number
  default     = 2
}

variable "enable_load_balancer" {
  description = "Enable Application Load Balancer (requires ELB service enabled in AWS account)"
  type        = bool
  default     = false
}

variable "import_existing_iam_role" {
  description = "Use existing IAM role instead of creating new one (set to true if IAM role already exists)"
  type        = bool
  default     = false
}

