import pathlib
from google.cloud import aiplatform
import kfp.dsl
from kfp import compiler
from tasks.components import Evaluator, Trainer


def gen_pipeline_fn(project: str):
    @kfp.dsl.pipeline(name="vertex-ai-template")
    def pipeline_fn(timestamp: str):
        trainer_task = Trainer(project=project).task(timestamp=timestamp)
        evaluator_task = Evaluator(project=project).task(
            model=trainer_task.model,
            timestamp=timestamp,
        )

    return pipeline_fn


def build(project: str, env: str):
    pipeline_path = f"build/pipelines/pipeline-{env}.yaml"
    pathlib.Path(pipeline_path).parent.mkdir(exist_ok=True, parents=True)
    compiler.Compiler().compile(
        pipeline_func=gen_pipeline_fn(project=project),
        package_path=pipeline_path,
    )


def run(project: str, env: str):
    job = aiplatform.PipelineJob(
        project=project,
        display_name="vertex-ai-template",
        template_path=f"build/pipelines/pipeline-{env}.yaml",
        parameter_values={},
        pipeline_root=f"gs://{project}-vertex/pipeline-root",
    )
    job.submit()
