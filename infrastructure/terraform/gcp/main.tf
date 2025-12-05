terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

# VPC Network
resource "google_compute_network" "main" {
  name                    = "codeforces-vpc"
  auto_create_subnetworks = false
}

# Subnet
resource "google_compute_subnetwork" "main" {
  name          = "codeforces-subnet"
  ip_cidr_range = "10.2.0.0/24"
  region        = var.gcp_region
  network       = google_compute_network.main.id
}

# GKE Cluster for Scoring, Leaderboard, and Frontend
resource "google_container_cluster" "main" {
  name     = "codeforces-gke-cluster"
  location = var.gcp_region

  remove_default_node_pool = true
  initial_node_count       = 1

  network    = google_compute_network.main.name
  subnetwork = google_compute_subnetwork.main.name

  master_auth {
    client_certificate_config {
      issue_client_certificate = false
    }
  }
}

resource "google_container_node_pool" "main" {
  name       = "codeforces-node-pool"
  location   = var.gcp_region
  cluster    = google_container_cluster.main.name
  node_count = 2

  node_config {
    preemptible  = false
    machine_type = "e2-medium"

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}

# Cloud Load Balancer
resource "google_compute_backend_service" "main" {
  name        = "codeforces-backend"
  protocol    = "HTTP"
  timeout_sec = 10

  health_checks = [google_compute_health_check.main.id]
}

resource "google_compute_health_check" "main" {
  name               = "codeforces-health-check"
  check_interval_sec = 5
  timeout_sec        = 3

  http_health_check {
    port         = 8000
    request_path = "/health"
  }
}

resource "google_compute_url_map" "main" {
  name            = "codeforces-url-map"
  default_service = google_compute_backend_service.main.id
}

resource "google_compute_target_https_proxy" "main" {
  name             = "codeforces-https-proxy"
  url_map          = google_compute_url_map.main.id
  ssl_certificates = [google_compute_managed_ssl_certificate.main.id]
}

resource "google_compute_global_forwarding_rule" "main" {
  name       = "codeforces-forwarding-rule"
  target     = google_compute_target_https_proxy.main.id
  port_range = "443"
  ip_address = google_compute_global_address.main.address
}

resource "google_compute_global_address" "main" {
  name = "codeforces-ip"
}

resource "google_compute_managed_ssl_certificate" "main" {
  name = "codeforces-ssl-cert"

  managed {
    domains = [var.domain_name]
  }
}

