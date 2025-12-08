output "aks_cluster_id" {
  description = "AKS cluster ID"
  value       = var.import_existing_aks_cluster ? data.azurerm_kubernetes_cluster.existing[0].id : azurerm_kubernetes_cluster.main[0].id
}

output "aks_cluster_fqdn" {
  description = "AKS cluster FQDN"
  value       = var.import_existing_aks_cluster ? data.azurerm_kubernetes_cluster.existing[0].fqdn : azurerm_kubernetes_cluster.main[0].fqdn
}

output "postgresql_fqdn" {
  description = "PostgreSQL FQDN"
  value       = local.postgres_server_fqdn
}

output "lb_public_ip" {
  description = "Load balancer public IP"
  value       = var.import_existing_public_ip ? data.azurerm_public_ip.existing[0].ip_address : (length(azurerm_public_ip.main) > 0 ? azurerm_public_ip.main[0].ip_address : "Pending")
}

output "lb_public_ip_id" {
  description = "Load balancer public IP resource ID"
  value       = local.public_ip_id
}

