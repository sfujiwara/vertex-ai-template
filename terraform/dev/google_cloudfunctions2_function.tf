resource "google_cloudfunctions2_function" "pipeline_runner" {
  name     = "pipeline-runner"
  project  = var.project
  location = "us-central1"
  build_config {
    entry_point = "main"
    runtime     = "python39"
    source {
      storage_source {
        bucket = google_storage_bucket.functions.name
        object = google_storage_bucket_object.pipeline_runner.name
      }
    }
  }
  service_config {
    available_memory   = "1024M"
    max_instance_count = 100
    timeout_seconds    = 180
    environment_variables = {
      GCP_PROJECT   = var.project
    }
  }
  labels = {
    terraform = ""
  }
  depends_on = [
    google_project_service.cloudbuild,
    google_project_service.cloudfunctions,
    google_project_service.run,
  ]
}
