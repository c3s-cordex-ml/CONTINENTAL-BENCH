# Contributing

Contributing a model to CONTINENTAL-BENCH takes two stages.

**Prepare your submission**, at your centre:

1. [Download the data](download.md) blocks of the experiments you take part in.
2. [Train your model](training.md).
3. [Prepare your predictions](predictions.md) for every test block, named after the DRS.
4. [Evaluate your predictions](evaluation.md) with ml-evaluation.
5. Write the training and inference configuration files of your model, in deep4production format, for its
   [reproducibility](reproducibility.md).

The [worked example](example.md) goes through these steps with a UNET trained with deep4production.

**[Submit your evaluation outputs](submission.md)**, together with your configuration files, through a pull request from
your own branch.

Experiment **A** is mandatory; **B** and **C** are optional. Predictions never leave your centre: only the evaluation outputs and
the configuration files are submitted.
