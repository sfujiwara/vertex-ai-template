resource "google_service_account" "vertex" {
  account_id   = "vertex"
  display_name = "Vertex AI"
  project      = var.project
}
