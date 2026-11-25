# Submit your evaluation outputs

Each model and experiment is submitted as one pull request, from a branch you create yourself.

The pull request adds:

```
EVALUATIONS/Experiment_<A|B|C>/<MODEL>/        # all evaluation cases, as produced in the previous step
REPRODUCIBILITY/Experiment_<A|B|C>/<MODEL>/    # train.yaml and inference.yaml
```

## Steps

1. Create a branch named `<MODEL>-<A|B|C>`:

    ```bash
    git checkout main && git pull
    git checkout -b UNET-A
    ```

2. Add your evaluation outputs and configuration files, and commit them:

    ```bash
    git add EVALUATIONS/Experiment_A/UNET REPRODUCIBILITY/Experiment_A/UNET
    git commit -m "Add UNET, experiment A"
    git push -u origin UNET-A
    ```

3. Open a pull request from your branch to `main`.

## Checklist

Before opening the pull request, check that:

- [ ] `<MODEL>` is the same in `EVALUATIONS/`, `REPRODUCIBILITY/` and in your prediction file names.
- [ ] Every evaluation case of the experiment is present, for every target variable and season.
- [ ] `train.yaml` and `inference.yaml` are in deep4production format and use relative paths.
- [ ] No prediction or data files (`*.nc`) are included.

Once the pull request is merged, the scoreboards are updated with the new model.
