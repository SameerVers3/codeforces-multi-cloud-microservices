terraform {
  required_version = ">= 1.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Data source to check if resource group exists (for import handling)
data "azurerm_resource_group" "existing" {
  count = var.import_existing_resource_group ? 1 : 0
  name  = "codeforces-rg"
}

# Resource Group
# If resource group already exists:
#   1. Set import_existing_resource_group = true, OR
#   2. Import it: terraform import azurerm_resource_group.main /subscriptions/{subscription-id}/resourceGroups/codeforces-rg, OR
#   3. Delete it: az group delete --name codeforces-rg --yes --no-wait
resource "azurerm_resource_group" "main" {
  count    = var.import_existing_resource_group ? 0 : 1
  name     = "codeforces-rg"
  location = var.azure_location

  tags = {
    ManagedBy = "Terraform"
  }
}

# Use existing resource group if importing, otherwise use created one
locals {
  resource_group_name = var.import_existing_resource_group ? data.azurerm_resource_group.existing[0].name : azurerm_resource_group.main[0].name
  resource_group_location = var.import_existing_resource_group ? data.azurerm_resource_group.existing[0].location : azurerm_resource_group.main[0].location
}

# Data source for existing virtual network (if importing)
data "azurerm_virtual_network" "existing" {
  count               = var.import_existing_vnet ? 1 : 0
  name                = "codeforces-vnet"
  resource_group_name = local.resource_group_name
}

# Virtual Network
# If VNet already exists, set import_existing_vnet = true
resource "azurerm_virtual_network" "main" {
  count               = var.import_existing_vnet ? 0 : 1
  name                = "codeforces-vnet"
  address_space       = ["10.1.0.0/16"]
  location            = local.resource_group_location
  resource_group_name = local.resource_group_name
}

# Data source for existing public IP (if importing)
data "azurerm_public_ip" "existing" {
  count               = var.import_existing_public_ip ? 1 : 0
  name                = "codeforces-lb-ip"
  resource_group_name = local.resource_group_name
}

# Load Balancer Public IP
# If public IP already exists, set import_existing_public_ip = true
resource "azurerm_public_ip" "main" {
  count               = var.import_existing_public_ip ? 0 : 1
  name                = "codeforces-lb-ip"
  location            = local.resource_group_location
  resource_group_name = local.resource_group_name
  allocation_method   = "Static"
  sku                 = "Standard"
}

# Use existing VNet and Public IP if importing, otherwise use created ones
locals {
  vnet_id = var.import_existing_vnet ? data.azurerm_virtual_network.existing[0].id : azurerm_virtual_network.main[0].id
  vnet_name = var.import_existing_vnet ? data.azurerm_virtual_network.existing[0].name : azurerm_virtual_network.main[0].name
  public_ip_id = var.import_existing_public_ip ? data.azurerm_public_ip.existing[0].id : azurerm_public_ip.main[0].id
}

# Subnet
resource "azurerm_subnet" "main" {
  name                 = "codeforces-subnet"
  resource_group_name  = local.resource_group_name
  virtual_network_name = local.vnet_name
  address_prefixes     = ["10.1.1.0/24"]
}

# AKS Cluster for Auth and Contest Services
resource "azurerm_kubernetes_cluster" "main" {
  name                = "codeforces-aks-cluster"
  location            = local.resource_group_location
  resource_group_name = local.resource_group_name
  dns_prefix          = "codeforces-aks"

  default_node_pool {
    name       = "default"
    node_count = 2
    vm_size    = "standard_dc2s_v3"  # Using available VM size for the subscription
  }

  identity {
    type = "SystemAssigned"
  }
}

# PostgreSQL Flexible Server (replaces deprecated azurerm_postgresql_server)
# Note: Flexible Server requires a dedicated subnet for database
resource "azurerm_subnet" "postgres" {
  name                 = "codeforces-postgres-subnet"
  resource_group_name  = local.resource_group_name
  virtual_network_name = local.vnet_name
  address_prefixes     = ["10.1.2.0/24"]
  
  delegation {
    name = "postgres-delegation"
    service_delegation {
      name = "Microsoft.DBforPostgreSQL/flexibleServers"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/join/action",
      ]
    }
  }
}

resource "azurerm_private_dns_zone" "main" {
  name                = "codeforces-postgres.postgres.database.azure.com"
  resource_group_name = local.resource_group_name
}

resource "azurerm_private_dns_zone_virtual_network_link" "main" {
  name                  = "codeforces-vnet-link"
  resource_group_name   = local.resource_group_name
  private_dns_zone_name = azurerm_private_dns_zone.main.name
  virtual_network_id    = local.vnet_id
}

resource "azurerm_postgresql_flexible_server" "main" {
  name                   = "codeforces-postgres"
  resource_group_name    = local.resource_group_name
  location               = local.resource_group_location
  version                = "11"
  delegated_subnet_id    = azurerm_subnet.postgres.id
  private_dns_zone_id    = azurerm_private_dns_zone.main.id
  administrator_login    = var.db_admin_login
  administrator_password = var.db_admin_password

  sku_name = "GP_Standard_D2s_v3"

  storage_mb = 32768

  backup_retention_days        = 7
  geo_redundant_backup_enabled = false

  depends_on = [azurerm_private_dns_zone_virtual_network_link.main]
}

resource "azurerm_postgresql_flexible_server_database" "main" {
  name      = "codeforces_db"
  server_id = azurerm_postgresql_flexible_server.main.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

# Load Balancer

resource "azurerm_lb" "main" {
  name                = "codeforces-lb"
  location            = local.resource_group_location
  resource_group_name = local.resource_group_name
  sku                 = "Standard"

  frontend_ip_configuration {
    name                 = "PublicIPAddress"
    public_ip_address_id = local.public_ip_id
  }
}

