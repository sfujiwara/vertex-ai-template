# Vertex AI Template

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue)](https://www.python.org)

A template for typical machine learning projects using Vertex AI.

## Architecture

```mermaid
flowchart LR
  scheduler(Cloud Scheduler) -- HTTP Request --> functions(Cloud Functions)
  functions --> vertex(Vertex AI Pipelines)
  registry(Artifact Registry) -. Pipeline YAML .-> vertex
  registry -. Dcoker Image .-> vertex
```

## Requirements

* Poetry
* Google Cloud SDK
* Terraform

## Installation

```shell
poetry install
```

```shell
poetry shell
```

## Deployment

### Terraform

Create Google Cloud Platform resources with Terraform:

```shell
inv terraform.init
```

```shell
inv terraform.apply
```

### Docker

Build Docker images for Vertex AI Pipelines components:

```shell
inv docker.build -f invoke-dev.yaml
```

Push Docker images:

```shell
inv docker.push -f invoke-dev.yaml
```

### Pipeline

Generate pipeline YAML with Kubeflow Pipelines SDK:

```shell
inv pipeline.build -f invoke-dev.yaml
```

Upload pipeline YAML to Google Cloud Artifact Registry:

```shell
inv pipeline.push -f invoke-dev.yaml
```
