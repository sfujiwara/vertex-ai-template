from pathlib import Path
import invoke


@invoke.task
def evaluate(ctx, model_dir, timestamp, deploy):
    """Execute training."""
    # Download training dataset.
    # d = download_eval_dataset(timestamp)

    # Execute evaluation.
    # ...

    Path(deploy).parent.mkdir(parents=True, exist_ok=True)
    with open(deploy, "w") as f:
        f.write(str(True))
