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

# Consolidate all locals - will be expanded after all data sources are defined

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

# Data source for existing subnet (if importing)
data "azurerm_subnet" "existing_main" {
  count                = var.import_existing_subnet_main ? 1 : 0
  name                 = "codeforces-subnet"
  resource_group_name  = local.resource_group_name
  virtual_network_name = local.vnet_name
}

# Subnet
# If subnet already exists, set import_existing_subnet_main = true
resource "azurerm_subnet" "main" {
  count                = var.import_existing_subnet_main ? 0 : 1
  name                 = "codeforces-subnet"
  resource_group_name  = local.resource_group_name
  virtual_network_name = local.vnet_name
  address_prefixes     = ["10.1.1.0/24"]
}

# Data source for existing AKS cluster (if importing)
data "azurerm_kubernetes_cluster" "existing" {
  count               = var.import_existing_aks_cluster ? 1 : 0
  name                = "codeforces-aks-cluster"
  resource_group_name = local.resource_group_name
}

# AKS Cluster for Auth and Contest Services
# If AKS cluster already exists, set import_existing_aks_cluster = true
resource "azurerm_kubernetes_cluster" "main" {
  count               = var.import_existing_aks_cluster ? 0 : 1
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
# Data source for existing postgres subnet (if importing)
data "azurerm_subnet" "existing_postgres" {
  count                = var.import_existing_subnet_postgres ? 1 : 0
  name                 = "codeforces-postgres-subnet"
  resource_group_name  = local.resource_group_name
  virtual_network_name = local.vnet_name
}

resource "azurerm_subnet" "postgres" {
  count                = var.import_existing_subnet_postgres ? 0 : 1
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

# Data source for existing private DNS zone (if importing)
# Note: DNS zone name must end with .postgres.database.azure.com (with a prefix)
data "azurerm_private_dns_zone" "existing" {
  count               = var.import_existing_dns_zone ? 1 : 0
  name                = "codeforces.postgres.database.azure.com"
  resource_group_name = local.resource_group_name
}

resource "azurerm_private_dns_zone" "main" {
  count               = var.import_existing_dns_zone ? 0 : 1
  name                = "codeforces.postgres.database.azure.com"
  resource_group_name = local.resource_group_name
}

# Consolidate all locals
locals {
  # Resource Group
  resource_group_name = var.import_existing_resource_group ? data.azurerm_resource_group.existing[0].name : azurerm_resource_group.main[0].name
  resource_group_location = var.import_existing_resource_group ? data.azurerm_resource_group.existing[0].location : azurerm_resource_group.main[0].location
  
  # VNet and Public IP
  vnet_id = var.import_existing_vnet ? data.azurerm_virtual_network.existing[0].id : azurerm_virtual_network.main[0].id
  vnet_name = var.import_existing_vnet ? data.azurerm_virtual_network.existing[0].name : azurerm_virtual_network.main[0].name
  public_ip_id = var.import_existing_public_ip ? data.azurerm_public_ip.existing[0].id : azurerm_public_ip.main[0].id
  
  # Subnets
  subnet_main_id = var.import_existing_subnet_main ? data.azurerm_subnet.existing_main[0].id : azurerm_subnet.main[0].id
  subnet_postgres_id = var.import_existing_subnet_postgres ? data.azurerm_subnet.existing_postgres[0].id : azurerm_subnet.postgres[0].id
  
  # DNS Zone
  dns_zone_id = var.import_existing_dns_zone ? data.azurerm_private_dns_zone.existing[0].id : azurerm_private_dns_zone.main[0].id
  dns_zone_name = var.import_existing_dns_zone ? data.azurerm_private_dns_zone.existing[0].name : azurerm_private_dns_zone.main[0].name
}

# Data source for existing DNS zone VNet link (if importing)
data "azurerm_private_dns_zone_virtual_network_link" "existing" {
  count                = var.import_existing_dns_vnet_link ? 1 : 0
  name                 = "codeforces-vnet-link"
  resource_group_name  = local.resource_group_name
  private_dns_zone_name = local.dns_zone_name
}

resource "azurerm_private_dns_zone_virtual_network_link" "main" {
  count                = var.import_existing_dns_vnet_link ? 0 : 1
  name                  = "codeforces-vnet-link"
  resource_group_name   = local.resource_group_name
  private_dns_zone_name = local.dns_zone_name
  virtual_network_id    = local.vnet_id
}

resource "azurerm_postgresql_flexible_server" "main" {
  name                   = "codeforces-postgres"
  resource_group_name    = local.resource_group_name
  location               = local.resource_group_location
  version                = "11"
  delegated_subnet_id           = local.subnet_postgres_id
  private_dns_zone_id           = local.dns_zone_id
  public_network_access_enabled = false
  administrator_login            = var.db_admin_login
  administrator_password         = var.db_admin_password

  sku_name = "GP_Standard_D2s_v3"

  storage_mb = 32768

  backup_retention_days        = 7
  geo_redundant_backup_enabled = false

  # Dependencies are handled automatically through private_dns_zone_id reference
}

resource "azurerm_postgresql_flexible_server_database" "main" {
  name      = "codeforces_db"
  server_id = azurerm_postgresql_flexible_server.main.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

# Load Balancer

# Data source for existing load balancer (if importing)
data "azurerm_lb" "existing" {
  count               = var.import_existing_lb ? 1 : 0
  name                = "codeforces-lb"
  resource_group_name = local.resource_group_name
}

# Load Balancer
# If load balancer already exists, set import_existing_lb = true
resource "azurerm_lb" "main" {
  count               = var.import_existing_lb ? 0 : 1
  name                = "codeforces-lb"
  location            = local.resource_group_location
  resource_group_name = local.resource_group_name
  sku                 = "Standard"

  frontend_ip_configuration {
    name                 = "PublicIPAddress"
    public_ip_address_id = local.public_ip_id
  }
}

