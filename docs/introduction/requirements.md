# Requirements

Two Python packages are needed, best installed in separate environments:

| Package | Used for |
|---|---|
| [deep4production](https://github.com/SantanderMetGroup/deep4production) | training the model (`d4p-train`) and producing the predictions (`d4p-downscale`) |
| [ml-evaluation](https://github.com/c3s-cordex-ml/ml-evaluation) | evaluating the predictions (`ml-eval`) |

Both can be installed with [Pixi](https://pixi.sh) or Conda. Training on GPU is strongly recommended.

## deep4production

```bash
git clone https://github.com/SantanderMetGroup/deep4production
cd deep4production
```

=== "Pixi"

    ```bash
    pixi install
    ```

=== "Conda"

    ```bash
    conda create -n deep4production python=3.12
    conda activate deep4production
    pip install -r requirements.txt
    pip install .
    ```

For GPU support, install the CUDA build of PyTorch that matches your system (see the deep4production README).

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
