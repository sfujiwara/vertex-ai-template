terraform {
  required_providers {
    google-beta = {
      version = "4.43.0"
    }
  }
}

provider "google-beta" {
  project = var.project
}
