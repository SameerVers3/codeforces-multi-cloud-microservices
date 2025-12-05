variable "azure_location" {
  description = "Azure location"
  type        = string
  default     = "eastus"
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

