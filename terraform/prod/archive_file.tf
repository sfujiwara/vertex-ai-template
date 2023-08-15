data "archive_file" "pipeline_runner" {
  type        = "zip"
  source_dir  = "../../functions"
  output_path = "pipeline-runner.zip"
}
