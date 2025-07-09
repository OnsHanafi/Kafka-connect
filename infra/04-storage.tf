resource "azurerm_storage_account" "this" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_kind              = "StorageV2"
  account_tier             = "Standard"
  account_replication_type = "GRS"
}

resource "azurerm_storage_container" "this" {
  name                  = "yalen-cluster-container-2025"
  storage_account_name  = azurerm_storage_account.this.name
  container_access_type = "private"
}

