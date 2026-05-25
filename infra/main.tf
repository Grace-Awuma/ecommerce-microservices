data "azurerm_client_config" "current" {}

# Resource Group
resource "azurerm_resource_group" "ecommerce" {
  name     = var.resource_group_name
  location = var.location
}

# Azure Container Registry
resource "azurerm_container_registry" "acr" {
  name                = var.acr_name
  resource_group_name = azurerm_resource_group.ecommerce.name
  location            = azurerm_resource_group.ecommerce.location
  sku                 = "Basic"
  admin_enabled       = true
}

# PostgreSQL for product service
resource "azurerm_postgresql_flexible_server" "product_db" {
  name                   = "ecommerce-product-db"
  resource_group_name    = azurerm_resource_group.ecommerce.name
  location               = var.db_location
  version                = "15"
  administrator_login    = "postgresadmin"
  administrator_password = azurerm_key_vault_secret.db_password.value
  sku_name               = "B_Standard_B1ms"
  storage_mb             = 32768
  backup_retention_days  = 7
   zone                   = "1"
}

resource "azurerm_postgresql_flexible_server_database" "product_db" {
  name      = "productdb"
  server_id = azurerm_postgresql_flexible_server.product_db.id
}

# PostgreSQL for order service
resource "azurerm_postgresql_flexible_server" "order_db" {
  name                   = "ecommerce-order-db-ne"
  resource_group_name    = azurerm_resource_group.ecommerce.name
  location               = var.db_location
  version                = "15"
  administrator_login    = "postgresadmin"
  administrator_password = azurerm_key_vault_secret.db_password.value
  sku_name               = "B_Standard_B1ms"
  storage_mb             = 32768
  backup_retention_days  = 7
  zone                   = "1"
}

resource "azurerm_postgresql_flexible_server_database" "order_db" {
  name      = "orderdb"
  server_id = azurerm_postgresql_flexible_server.order_db.id
}

# PostgreSQL for payment service
resource "azurerm_postgresql_flexible_server" "payment_db" {
  name                   = "ecommerce-payment-db-ne"
  resource_group_name    = azurerm_resource_group.ecommerce.name
  location               = var.db_location
  version                = "15"
  administrator_login    = "postgresadmin"
  administrator_password = azurerm_key_vault_secret.db_password.value
  sku_name               = "B_Standard_B1ms"
  storage_mb             = 32768
  backup_retention_days  = 7
  zone                   = "1"
}

resource "azurerm_postgresql_flexible_server_database" "payment_db" {
  name      = "paymentdb"
  server_id = azurerm_postgresql_flexible_server.payment_db.id
}

# AKS Cluster
resource "azurerm_kubernetes_cluster" "aks" {
  name                = var.cluster_name
  location = azurerm_resource_group.ecommerce.location
  resource_group_name = azurerm_resource_group.ecommerce.name
  dns_prefix          = var.cluster_name
  kubernetes_version  = var.kubernetes_version
  support_plan        = "KubernetesOfficial"

  default_node_pool {
    name       = "default"
    node_count = var.node_count
    vm_size    = var.node_vm_size
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin = "kubenet"
    dns_service_ip = "10.0.0.10"
    service_cidr   = "10.0.0.0/16"
  }

  tags = {
    environment = "dev"
    project     = "ecommerce-microservices"
  }
}

# Allow AKS to pull images from ACR
resource "azurerm_role_assignment" "aks_acr_pull" {
  principal_id                     = azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id
  role_definition_name             = "AcrPull"
  scope                            = azurerm_container_registry.acr.id
  skip_service_principal_aad_check = true
}

# Key Vault
resource "azurerm_key_vault" "ecommerce" {
  name                = "ecommerce-kv-grace"
  location            = azurerm_resource_group.ecommerce.location
  resource_group_name = azurerm_resource_group.ecommerce.name
  tenant_id           = var.tenant_id
  sku_name            = "standard"

  access_policy {
    tenant_id = var.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    secret_permissions = [
      "Get", "Set", "List", "Delete"
    ]
  }
}

# Store DB password as secret
resource "azurerm_key_vault_secret" "db_password" {
  name         = "db-password"
  value        = var.db_password
  key_vault_id = azurerm_key_vault.ecommerce.id
}

resource "azurerm_postgresql_flexible_server_firewall_rule" "product_db" {
  name             = "allow-aks"
  server_id        = azurerm_postgresql_flexible_server.product_db.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "255.255.255.255"
}

resource "azurerm_postgresql_flexible_server_firewall_rule" "order_db" {
  name             = "allow-aks"
  server_id        = azurerm_postgresql_flexible_server.order_db.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "255.255.255.255"
}

resource "azurerm_postgresql_flexible_server_firewall_rule" "payment_db" {
  name             = "allow-aks"
  server_id        = azurerm_postgresql_flexible_server.payment_db.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "255.255.255.255"
}