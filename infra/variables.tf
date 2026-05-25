variable "subscription_id" {
  description = "Azure subscription ID"
  type        = string
  default     = "fe79b717-7a74-4ada-9446-adfd09d26127"
}

variable "tenant_id" {
  description = "Azure tenant ID"
  type        = string
  default     = "83c95635-0459-4c20-9208-f3d7d5ca76ee"
}

variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
  default     = "ecommerce-rg"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "West Europe"
}

variable "cluster_name" {
  description = "AKS cluster name"
  type        = string
  default     = "ecommerce-aks"
}

variable "acr_name" {
  description = "Azure Container Registry name (must be globally unique, lowercase, no hyphens)"
  type        = string
  default     = "gracecommerceacr"
}

variable "node_count" {
  description = "Number of nodes in the AKS cluster"
  type        = number
  default     = 1
}

variable "node_vm_size" {
  description = "VM size for AKS nodes"
  type        = string
  default     = "Standard_B2s_v2"
}

variable "kubernetes_version" {
  description = "Kubernetes version"
  type        = string
  default     = "1.33"
}

variable "db_password" {
  description = "PostgreSQL administrator password"
  type        = string
  sensitive   = true
}

variable "db_location" {
  description = "Location for PostgreSQL databases"
  type        = string
  default     = "North Europe"
}