import invoke


@invoke.task
def train(ctx, model_dir, dataset):
    """Execute training."""
    # Download training dataset.
    # d = download_dataset(dataset)

    # Execute training.
    # ...

