output "gke_cluster_id" {
  description = "GKE cluster ID"
  value       = google_container_cluster.main.id
}

output "gke_cluster_endpoint" {
  description = "GKE cluster endpoint"
  value       = google_container_cluster.main.endpoint
}

output "load_balancer_ip" {
  description = "Load balancer IP address"
  value       = google_compute_global_address.main.address
}

output "gke_cluster_name" {
  description = "GKE cluster name"
  value       = google_container_cluster.main.name
}

