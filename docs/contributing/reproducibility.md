# Reproducibility

The exact configuration used to train and to apply the submitted model is part of the submission, written in the YAML format of
[deep4production](https://github.com/SantanderMetGroup/deep4production), whatever framework you trained with:

```
REPRODUCIBILITY/
└── Experiment_<A|B|C>/
    └── <institution_id>-<emulator_id>/   # as in the prediction file names, e.g. CSIC-CorrDiff; also used in EVALUATIONS/
        ├── train.yaml      # the configuration the submitted model was trained with
        └── inference.yaml  # example: ERA5 imperfect predictors, block ERA5/1981-2000
```

- Exactly one `train.yaml` and one `inference.yaml` per model and experiment; overwrite them when you retrain.
- `inference.yaml` is the ERA5-imperfect case only; the other test cases differ just in the input data and output file.
- Paths are relative to the root of the repository, never absolute to your filesystem.
- The folder is named `<institution_id>-<emulator_id>`, with the two facets of your prediction file names (e.g. `CSIC-CorrDiff`,
  `UiB-CorrDiff`).
