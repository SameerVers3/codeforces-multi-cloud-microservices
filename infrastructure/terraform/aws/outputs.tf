output "eks_cluster_id" {
  description = "EKS cluster ID"
  value       = var.import_existing_eks_cluster ? data.aws_eks_cluster.existing[0].id : aws_eks_cluster.main[0].id
}

output "eks_cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = var.import_existing_eks_cluster ? data.aws_eks_cluster.existing[0].endpoint : aws_eks_cluster.main[0].endpoint
}

output "alb_dns_name" {
  description = "ALB DNS name"
  value       = var.enable_load_balancer ? aws_lb.main[0].dns_name : null
}

output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

