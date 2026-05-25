terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }

  backend "azurerm" {
    resource_group_name  = "ecommerce-tfstate-rg"
    storage_account_name = "graceawumtfstate"
    container_name       = "tfstate"
    key                  = "ecommerce.terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}