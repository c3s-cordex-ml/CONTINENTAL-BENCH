# Requirements

The evaluation uses two Python packages, both under development:

| Package | Used for |
|---|---|
| [ml-evaluation](https://github.com/c3s-cordex-ml/ml-evaluation) | the indices and diagnostics (`indices.py`, `diagnostics.py`) |
| [ml_c3s384_evaluation](https://github.com/c3s-cordex-ml/ml_c3s384_evaluation) | the command-line tools that run those indices and diagnostics for this benchmark |

Install both in the same environment, ml-evaluation first.

## ml-evaluation

```bash
git clone https://github.com/c3s-cordex-ml/ml-evaluation
cd ml-evaluation
```

=== "Pixi"

    ```bash
    pixi install
    ```

=== "Conda"

    ```bash
    conda env create -f environment.yaml
    conda activate ml-evaluation
    pip install -e .
    ```

A Docker image definition (`Dockerfile`) is also provided in the ml-evaluation repository.

## ml_c3s384_evaluation

In the ml-evaluation environment:

```bash
git clone https://github.com/c3s-cordex-ml/ml_c3s384_evaluation
cd ml_c3s384_evaluation
pip install -e .
```

Both packages are installed in editable mode (`-e`), so `git pull` in each repository is enough to get the latest version.
