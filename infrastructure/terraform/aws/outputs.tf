output "eks_cluster_id" {
  description = "EKS cluster ID"
  value       = aws_eks_cluster.main.id
}

output "eks_cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = aws_eks_cluster.main.endpoint
}

output "alb_dns_name" {
  description = "ALB DNS name"
  value       = var.enable_load_balancer ? aws_lb.main[0].dns_name : null
}

output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

