variable "subscription_id" {
  description = "The ID of the Azure subscription where resources will be created."
  type        = string
  
}
variable "tenant_id" {
  description = "The ID of the Azure tenant where resources will be created."
  type        = string

}

variable "resource_group_name" {
  default = "rg-yalen"
}

variable "location" {
  description = "The Azure region where resources will be created."
  type        = string
  default     = "francecentral"
  
}

variable "storage_account_name" {
  description = "The name of the Azure Storage Account."
  type        = string
  default     = "yalenclusterhdistorage"
  
}