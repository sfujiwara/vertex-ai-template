resource "google_project_iam_member" "vertex" {
  project = var.project
  role    = "roles/run.invoker"
  member  = google_service_account.vertex.member
}
