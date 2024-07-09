# Define the provider
provider "azurerm" {
  features {}
  subscription_id = "23a27e59-9630-46e7-a345-9a520d4a36f7"  
}

# Resource Group
resource "azurerm_resource_group" "rg" {
  name     = "Streamlit_poc"
  location = "West Europe"
}

# Azure Container Registry
resource "azurerm_container_registry" "acr" {
  name                = "streamlitACR_POC"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Standard"
  admin_enabled       = true

  tags = {
    environment = "dev"
  }
}

# App Service Plan
resource "azurerm_service_plan" "asp" {
  name                = "streamlit-asp"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  sku_name            = "S1"

  tags = {
    environment = "dev"
  }
}

# Web App
resource "azurerm_linux_web_app" "webapp" {
  name                = "streamlit-webapp"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  service_plan_id     = azurerm_service_plan.asp.id

  site_config {
    always_on = true
  }

  app_settings = {
    WEBSITES_ENABLE_APP_SERVICE_STORAGE = "false"
    DOCKER_REGISTRY_SERVER_URL          = "https://${azurerm_container_registry.acr.login_server}"
    DOCKER_REGISTRY_SERVER_USERNAME     = azurerm_container_registry.acr.admin_username
    DOCKER_REGISTRY_SERVER_PASSWORD     = azurerm_container_registry.acr.admin_password
    DOCKER_ENABLE_CI                    = "true"
  }

  tags = {
    environment = "dev"
  }
}
