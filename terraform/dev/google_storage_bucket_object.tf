resource "google_storage_bucket_object" "pipeline_runner" {
  name   = "cron-${data.archive_file.pipeline_runner.output_md5}.zip"
  bucket = google_storage_bucket.functions.name
  source = data.archive_file.pipeline_runner.output_path
}
