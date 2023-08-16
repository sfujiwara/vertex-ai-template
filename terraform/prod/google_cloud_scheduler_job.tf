resource "google_cloud_scheduler_job" "pipeline_trigger" {
  name        = "pipeline-trigger"
  description = "Trigger Vertex Pipelines."
  schedule    = "0 2 * * *"
  project     = var.project
  region      = "us-central1"
  time_zone   = "Asia/Tokyo"
  http_target {
    http_method = "POST"
    uri         = google_cloudfunctions2_function.pipeline_runner.service_config[0].uri
    oidc_token {
      service_account_email = google_service_account.vertex.email
    }
  }
  retry_config {
    retry_count = 5
  }
  depends_on = [google_project_service.cloudscheduler]
}
