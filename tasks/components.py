from kfp.components import load_component_from_text
import kfp
import yaml
from kfp import dsl
from kfp.dsl import Input, Model, OutputPath


@dsl.component
def deployer():
    pass


class Evaluator:
    def __init__(self, project) -> None:
        self.image = f"us-central1-docker.pkg.dev/{project}/docker/evaluator:latest"
        self.op = None

    def task(self, model, timestamp):
        @kfp.dsl.container_component
        def evaluator(model: Input[Model], timestamp: str, deploy: OutputPath(bool)):
            container_spec = kfp.dsl.ContainerSpec(
                image=self.image,
                command=["inv", "evaluate"],
                args=[
                    "--model-dir",
                    model.uri,
                    "--timestamp",
                    timestamp,
                    "--deploy",
                    deploy,
                ],
            )
            return container_spec

        self.op = evaluator(model=model, timestamp=timestamp)

        return self

    @property
    def deploy(self):
        return self.op.output


class Trainer:
    def __init__(self, project: str, name: str = "trainer"):
        self.name = name
        self.op = None
        self.dict = {
            "name": name,
            "inputs": [
                {"name": "timestamp", "type": "String"},
            ],
            "outputs": [
                {"name": "model", "type": "Model"},
            ],
            "implementation": {
                "container": {
                    "image": f"us-central1-docker.pkg.dev/{project}/docker/trainer:latest",
                    "command": ["inv", "train"],
                    "args": [
                        "--model-dir",
                        {"outputPath": "model"},
                        "--timestamp",
                        {"inputValue": "timestamp"}
                    ],
                },
            }
        }

    def task(self, timestamp: str):
        self.op = load_component_from_text(yaml.dump(self.dict))(timestamp=timestamp)
        return self

    @property
    def model(self):
        return self.op.outputs["model"]
