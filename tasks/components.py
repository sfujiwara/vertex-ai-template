from kfp.components import load_component_from_text
import yaml


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
