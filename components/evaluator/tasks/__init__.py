from pathlib import Path
import invoke


@invoke.task
def evaluate(ctx, model_dir, timestamp, output_param):
    """Execute training."""
    # Download training dataset.
    # d = download_eval_dataset(timestamp)

    # Execute evaluation.
    # ...

    Path(output_param).parent.mkdir(parents=True, exist_ok=True)
    with open(output_param, "w") as f:
        f.write(str(True))
