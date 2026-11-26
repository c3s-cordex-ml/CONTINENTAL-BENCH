# Experiments

Each model is trained in one or more **training experiments** and then applied to a common set of test blocks, which defines the
**prediction experiments**.

### Training experiments

There is one mandatory training experiment and two optional ones. They differ only in the training data; training always uses
**perfect** predictors.

| Experiment | Status | Training blocks | Training years |
|---|---|---|---|
| **A** | mandatory | EC-Earth3-Veg 1961-1980, 2080-2099 | 40 |
| **B** | optional | EC-Earth3-Veg 1961-1980, 2001-2014, 2015-2040, 2061-2079, 2080-2099 | 99 |
| **C** | optional | EC-Earth3-Veg, MPI-ESM1-2-HR and NorESM2-MM, each 1961-1980 and 2080-2099 | 3 × 40 |

- **A** learns the present and the end-of-century climate of a single simulation. The mid-century test period lies *between* the
  two training periods.
- **B** uses every year of the EC-Earth3-Veg simulation except the test periods (1981-2000 and 2041-2060), to measure the gain of
  a longer training set.
- **C** uses the periods of A from the three GCM-driven simulations, to measure the gain of training on several driving models.

#### Validation years

The same four years are held out from the training blocks for validation (early stopping, model selection) in all experiments:
**1967, 1975, 2087 and 2095**. In experiment C they are held out from each of the three simulations.

### Prediction experiments

Every model trained in a training experiment is applied to the same **test blocks**, with perfect and, where available,
imperfect predictors:

| Test | Block | Perfect | Imperfect |
|---|---|---|---|
| Historical | EC-Earth3-Veg/1981-2000 | ✔ | *pending* |
| | MPI-ESM1-2-HR/1981-2000 | ✔ | ✔ |
| | NorESM2-MM/1981-2000 | ✔ | ✔ |
| Mid-century | EC-Earth3-Veg/2041-2060 | <span class="skill">✔</span> | ✔ |
| | MPI-ESM1-2-HR/2041-2060 | ✔ | ✔ |
| | NorESM2-MM/2041-2060 | ✔ | ✔ |
| Evaluation | ERA5/1981-2000 | <span class="skill">✔</span> | <span class="skill">✔</span> |

*Test blocks to predict with each model, by type of predictors. Red <span class="skill">✔</span>: downscaling skill and
transferability experiments; black ✔: climate-change signal analysis.*

That is 13 predictions per model and training experiment (14 once the EC-Earth3-Veg historical imperfect predictors are
available), each covering the 11 target variables with **1 member** (deterministic models) or **5 members** (ensembles) (see
[Prepare your predictions](../contributing/predictions.md)). They make up four prediction experiments.

#### Downscaling skill (perfect)

EC-Earth3-Veg 2041-2060 with perfect predictors, compared with RegCM5-0 driven by EC-Earth3-Veg. It measures how well the model
reproduces the regional simulation it was trained on, in a period not seen in training.

#### Transferability of the downscaling (perfect)

ERA5 1981-2000 with perfect predictors, compared with RegCM5-0 driven by ERA5. It measures how well the model transfers to a
driving model not seen in training.

#### Transferability of the downscaling (imperfect)

ERA5 1981-2000 with imperfect predictors (the ERA5 reanalysis itself), compared with ERA5-Land. It measures how well the model
performs when applied to real large-scale predictors, against observations.

#### Climate change signal analysis

The 1981-2000 and 2041-2060 blocks of the three GCMs, with perfect and imperfect predictors. The climate-change signal
(2041-2060 minus 1981-2000) of each prediction is compared with that of RegCM5-0 driven by the same GCM, which gives an ensemble
of three perfect and, for now, two imperfect members.

Predictions stay at each centre: they are neither uploaded to GitHub nor shared. Only their evaluation outputs are submitted
(see [Contributing](../contributing/index.md)).
