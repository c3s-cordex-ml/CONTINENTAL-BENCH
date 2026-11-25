# Train your model

Models are trained with [deep4production](https://github.com/SantanderMetGroup/deep4production) (`d4p-train`), on the
**perfect** predictors and the targets of the training blocks of each experiment (see [Experiments](../introduction/experiments.md)).
The architecture is free.

Things to keep in mind:

- Cells outside the RegCM5-0 domain are NaN in the perfect predictors. Your model must handle them, e.g. by setting them to zero
  after normalisation; at inference, apply the same mask to the imperfect predictors.
- Validation years: *TBD*.
- Use the same architecture and training set-up for all target variables of a model. A different approach is a different model,
  with its own name.

## Configuration files

The exact configuration used to train and to apply the submitted model is part of the submission, in deep4production YAML format:

```
REPRODUCIBILITY/
└── Experiment_<A|B|C>/
    └── <MODEL>/            # same <MODEL> name as in EVALUATIONS/ and in the prediction files
        ├── train.yaml      # the configuration the submitted model was trained with
        └── inference.yaml  # example: ERA5 imperfect predictors, block ERA5/1981-2000
```

- Exactly one `train.yaml` and one `inference.yaml` per model and experiment; overwrite them when you retrain.
- `inference.yaml` is the ERA5-imperfect case only; the other test cases differ just in the input data and output file.
- Paths are relative to the root of the repository, never absolute to your filesystem.
- `<MODEL>` may contain letters, digits and `-`, but no `_` (it is a facet of the DRS file names).
