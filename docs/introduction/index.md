# Introduction

CONTINENTAL-BENCH asks a machine-learning model to map **coarse upper-air fields** (the *predictors*, on a 1° grid)
onto the **daily surface output of RegCM5-0 at 0.11°** (the *targets*, on the native EUR-12 grid).

- [Data](data.md): the regional simulations, the predictors, the targets and how the files are organised.
- [Experiments](experiments.md): the three training set-ups (A, B, C).
- [Predictions](predictions.md): which predictions each trained model must produce.
- [Evaluation](evaluation.md): which metrics are computed on those predictions and against which reference.
- [Requirements](requirements.md): the software needed to train, predict and evaluate.
