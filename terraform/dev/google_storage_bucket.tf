resource "google_storage_bucket" "functions" {
  name                        = "${var.project}-functions"
  location                    = "US-CENTRAL1"
  project                     = var.project
  storage_class               = "REGIONAL"
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "vertex" {
  name                        = "${var.project}-vertex"
  location                    = "US-CENTRAL1"
  project                     = var.project
  storage_class               = "REGIONAL"
  uniform_bucket_level_access = true
}
