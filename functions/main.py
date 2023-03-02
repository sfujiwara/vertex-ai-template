import os
import functions_framework
from google.cloud import aiplatform


@functions_framework.http
def main(request):
    project = os.environ.get("GCP_PROJECT")
    template_path = f"https://us-central1-kfp.pkg.dev/{project}/kfp/vertex-ai-template/latest"

    job = aiplatform.PipelineJob(
        display_name="sample-pipeline",
        template_path=template_path,
        pipeline_root=f"gs://{project}-vertex/pipeline-root",
        enable_caching=False,
        parameter_values={
            "dataset": "dataset",
        },
    )
    job.submit(create_request_timeout=60)

    return "ok"
