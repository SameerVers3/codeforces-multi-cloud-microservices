variable "azure_location" {
  description = "Azure location"
  type        = string
  default     = "westus2"  # Changed from eastus due to quota restrictions
}

variable "resource_group_name" {
  description = "Resource group name"
  type        = string
  default     = "codeforces-rg"
}

variable "db_admin_login" {
  description = "Database admin login"
  type        = string
  sensitive   = true
}

variable "db_admin_password" {
  description = "Database admin password"
  type        = string
  sensitive   = true
}

variable "aks_node_count" {
  description = "Number of AKS nodes"
  type        = number
  default     = 2
}

variable "aks_vm_size" {
  description = "VM size for AKS nodes"
  type        = string
  default     = "Standard_D2s_v3"
}

variable "import_existing_resource_group" {
  description = "Import existing resource group instead of creating new one (set to true if resource group already exists)"
  type        = bool
  default     = false
}

variable "import_existing_vnet" {
  description = "Use existing virtual network instead of creating new one (set to true if VNet already exists)"
  type        = bool
  default     = false
}

variable "import_existing_public_ip" {
  description = "Use existing public IP instead of creating new one (set to true if public IP already exists)"
  type        = bool
  default     = false
}

variable "import_existing_subnet_main" {
  description = "Use existing main subnet instead of creating new one (set to true if subnet already exists)"
  type        = bool
  default     = false
}

variable "import_existing_subnet_postgres" {
  description = "Use existing postgres subnet instead of creating new one (set to true if subnet already exists)"
  type        = bool
  default     = false
}

variable "import_existing_aks_cluster" {
  description = "Use existing AKS cluster instead of creating new one (set to true if AKS cluster already exists)"
  type        = bool
  default     = false
}

variable "import_existing_dns_zone" {
  description = "Use existing private DNS zone instead of creating new one (set to true if DNS zone already exists)"
  type        = bool
  default     = false
}

variable "import_existing_lb" {
  description = "Use existing load balancer instead of creating new one (set to true if load balancer already exists)"
  type        = bool
  default     = false
}

variable "import_existing_dns_vnet_link" {
  description = "Use existing DNS zone VNet link instead of creating new one (set to true if link already exists)"
  type        = bool
  default     = false
}

variable "import_existing_postgres" {
  description = "Use existing PostgreSQL server instead of creating new one. Set to true if server already exists, false to create new. Defaults to true since server exists in eastus."
  type        = bool
  default     = true  # Changed to true since the server already exists in eastus
}

