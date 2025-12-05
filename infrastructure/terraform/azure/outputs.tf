output "aks_cluster_id" {
  description = "AKS cluster ID"
  value       = azurerm_kubernetes_cluster.main.id
}

output "aks_cluster_fqdn" {
  description = "AKS cluster FQDN"
  value       = azurerm_kubernetes_cluster.main.fqdn
}

output "postgresql_fqdn" {
  description = "PostgreSQL FQDN"
  value       = azurerm_postgresql_flexible_server.main.fqdn
}

output "lb_public_ip" {
  description = "Load balancer public IP"
  value       = var.import_existing_public_ip ? data.azurerm_public_ip.existing[0].ip_address : (length(azurerm_public_ip.main) > 0 ? azurerm_public_ip.main[0].ip_address : null)
}

