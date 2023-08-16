from kfp.components import load_component_from_text
import kfp
import yaml
from kfp.dsl import Input, Output, Dataset, Model


class Evaluator:
    def __init__(self, project) -> None:
        self.image = f"us-central1-docker.pkg.dev/{project}/docker/evaluator:latest"

    def task(self, model, dataset):
        @kfp.dsl.container_component
        def evaluator(model: Input[Model], dataset: str):
            container_spec = kfp.dsl.ContainerSpec(
                image=self.image,
                command=["inv", "evaluate"],
                args=["--model-dir", model.uri, "--dataset", dataset],
            )
            return container_spec

        evaluator(model=model, dataset=dataset)


class Trainer:
    def __init__(self, project: str, name: str = "trainer"):
        self.name = name
        self.op = None
        self.dict = {
            "name": name,
            "inputs": [
                {"name": "dataset", "type": "String"},
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
                        "--dataset",
                        {"inputValue": "dataset"}
                    ],
                },
            }
        }

    def task(self, dataset: str):
        self.op = load_component_from_text(yaml.dump(self.dict))(dataset=dataset)
        return self

    @property
    def model(self):
        return self.op.outputs["model"]
