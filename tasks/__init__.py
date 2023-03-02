import invoke
from kfp.registry import RegistryClient
import toml
from tasks import pipeline


def get_version() -> str:
    """Get version from `pyproject.toml`."""
    with open("pyproject.toml") as f:
        pyproject = toml.load(f)

    return pyproject["tool"]["poetry"]["version"]


@invoke.task
def pipeline_build(ctx):
    """Generate pipeline YAML for Vertex AI Pipelines."""
    env = ctx.config.run.env.name
    project = ctx.config.run.env.project
    pipeline.build(project=project, env=env)


@invoke.task
def pipeline_push(ctx):
    """Generate and upload pipeline YAML to Google Artifact Registry."""
    project = ctx.config.run.env.project
    env = ctx.config.run.env.name
    pipeline_build(ctx)
    client = RegistryClient(host=f"https://us-central1-kfp.pkg.dev/{project}/kfp")
    client.upload_pipeline(
        file_name=f"build/pipelines/pipeline-{env}.yaml",
        tags=["latest", get_version()],
    )


@invoke.task
def pipeline_run(ctx):
    """Submit Vertex AI Pipelines job from local environment."""
    env = ctx.config.run.env.name
    project = ctx.config.run.env.project
    pipeline_build(ctx)
    pipeline.run(project=project, env=env)


@invoke.task
def docker_build(ctx):
    """Build Docker images for Vertex AI Pipelines components."""
    project = ctx.config.run.env.project
    env = ctx.config.run.env.name
    ctx.run(f"PROJECT={project} TAG=latest docker-compose build")
    ctx.run(f"PROJECT={project} TAG={get_version()} docker-compose build")


@invoke.task
def docker_push(ctx):
    """Build and push Docker images for Vertex Pipelines components."""
    docker_build(ctx)
    project = ctx.config.run.env.project
    env = ctx.config.run.env.name
    ctx.run(f"PROJECT={project} TAG=latest docker-compose push")
    ctx.run(f"PROJECT={project} TAG={get_version()} docker-compose push")


@invoke.task
def terraform_init(ctx):
    """Execute terraform init command."""
    env = ctx.config.run.env.name

    with ctx.cd(f"terraform/{env}"):
        ctx.run(f"terraform init")


@invoke.task
def terraform_apply(ctx):
    """Execute terraform apply command."""
    project = ctx.config.run.env.project
    env = ctx.config.run.env.name

    with ctx.cd(f"terraform/{env}"):
        ctx.run(f"TF_VAR_project={project} terraform apply")


@invoke.task
def terraform_destroy(ctx):
    """Execute terraform destroy command."""
    project = ctx.config.run.env.project
    env = ctx.config.run.env.name

    with ctx.cd(f"terraform/{env}"):
        ctx.run(f"TF_VAR_project={project} terraform destroy")


@invoke.task
def deploy(ctx):
    """Execute all tasks for deployment"""
    terraform_apply(ctx)
    pipeline_build(ctx)
    pipeline_push(ctx)
    docker_build(ctx)
    docker_push(ctx)


p = invoke.Collection("pipeline")
p.add_task(pipeline_build, name="build")
p.add_task(pipeline_run, name="run")
p.add_task(pipeline_push, name="push")

d = invoke.Collection("docker")
d.add_task(docker_build, name="build")
d.add_task(docker_push, name="push")

t = invoke.Collection("terraform")
t.add_task(terraform_apply, name="apply")
t.add_task(terraform_init, name="init")

ns = invoke.Collection()
ns.add_collection(p)
ns.add_collection(d)
ns.add_collection(t)
ns.add_task(deploy, name="deploy")
