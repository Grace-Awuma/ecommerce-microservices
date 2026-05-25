output "resource_group_name" {
  value       = azurerm_resource_group.ecommerce.name
  description = "Resource group name"
}

output "acr_login_server" {
  value       = azurerm_container_registry.acr.login_server
  description = "ACR login server URL"
}

output "acr_name" {
  value       = azurerm_container_registry.acr.name
  description = "ACR name — replace <your-acr-name> in deployment.yaml files with this"
}

output "aks_cluster_name" {
  value       = azurerm_kubernetes_cluster.aks.name
  description = "AKS cluster name"
}

output "aks_cluster_id" {
  value       = azurerm_kubernetes_cluster.aks.id
  description = "AKS cluster ID"
}

output "get_credentials_command" {
  value       = "az aks get-credentials --resource-group ${azurerm_resource_group.ecommerce.name} --name ${azurerm_kubernetes_cluster.aks.name}"
  description = "Run this to connect kubectl to your AKS cluster"
}

output "product_db_host" {
  value       = azurerm_postgresql_flexible_server.product_db.fqdn
  description = "Product DB hostname"
}

output "order_db_host" {
  value       = azurerm_postgresql_flexible_server.order_db.fqdn
  description = "Order DB hostname"
}

output "payment_db_host" {
  value       = azurerm_postgresql_flexible_server.payment_db.fqdn
  description = "Payment DB hostname"
}