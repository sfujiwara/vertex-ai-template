import invoke


@invoke.task
def train(ctx, model_dir, timestamp):
    """Execute training."""
    # Download training dataset.
    # d = download_train_dataset(timestamp)

    # Execute training.
    # ...
