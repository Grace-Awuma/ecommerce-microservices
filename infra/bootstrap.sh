#!/bin/bash
# bootstrap.sh
# Run this ONCE before terraform init
# Creates the Azure storage backend for Terraform state

set -e

RESOURCE_GROUP="ecommerce-tfstate-rg"
STORAGE_ACCOUNT="graceawumtfstate"
CONTAINER_NAME="tfstate"
LOCATION="West Europe"

echo "Creating resource group for Terraform state..."
az group create \
  --name $RESOURCE_GROUP \
  --location "$LOCATION"

echo "Creating storage account..."
az storage account create \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --location "$LOCATION" \
  --sku Standard_LRS \
  --encryption-services blob

echo "Creating blob container..."
az storage container create \
  --name $CONTAINER_NAME \
  --account-name $STORAGE_ACCOUNT

echo ""
echo "Bootstrap complete! Backend storage is ready."
echo "You can now run:"
echo "  terraform init"
echo "  terraform plan -var-file=environments/dev.tfvars"
echo "  terraform apply -var-file=environments/dev.tfvars"