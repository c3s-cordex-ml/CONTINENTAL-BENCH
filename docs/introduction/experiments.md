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

Every model trained in a training experiment is applied to the [test blocks](#test-blocks) in three types of prediction
experiments.

#### 1. Period transferability {#exp-1}

A period not seen in training (2041-2060), with the same driving GCM as in training.

- **Block:** EC-Earth3-Veg/2041-2060, perfect predictors.

#### 2. Driver transferability {#exp-2}

A driver not seen in training: the ERA5 reanalysis.

- **2a. Perfect:** block ERA5/1981-2000, perfect predictors (RegCM5-0 driven by ERA5, upscaled to 1°).
- **2b. Imperfect:** block ERA5/1981-2000, imperfect predictors (the ERA5 reanalysis itself).

#### 3. Period and GCM transferability {#exp-3}

Two periods not seen in training (1981-2000 and 2041-2060) and driving GCMs not seen in training.

- **Blocks:** 1981-2000 and 2041-2060 of EC-Earth3-Veg, MPI-ESM1-2-HR and NorESM2-MM, with perfect and imperfect predictors.

#### Test blocks {#test-blocks}

Each cell gives the prediction experiments that use the prediction of that block with that type of predictors:

| Block | Perfect | Imperfect |
|---|---|---|
| EC-Earth3-Veg/1981-2000 | [3](#exp-3) | *pending* |
| MPI-ESM1-2-HR/1981-2000 | [3](#exp-3) | [3](#exp-3) |
| NorESM2-MM/1981-2000 | [3](#exp-3) | [3](#exp-3) |
| EC-Earth3-Veg/2041-2060 | <span class="skill">[1](#exp-1)</span>, [3](#exp-3) | [3](#exp-3) |
| MPI-ESM1-2-HR/2041-2060 | [3](#exp-3) | [3](#exp-3) |
| NorESM2-MM/2041-2060 | [3](#exp-3) | [3](#exp-3) |
| ERA5/1981-2000 | <span class="skill">[2a](#exp-2)</span> | <span class="skill">[2b](#exp-2)</span> |

That is 13 predictions per model and training experiment (14 once the EC-Earth3-Veg historical imperfect predictors are
available), each covering the 11 target variables with **1 member** (deterministic models) or **5 members** (ensembles) (see
[Prepare your predictions](../contributing/predictions.md)).

Predictions stay at each centre: they are neither uploaded to GitHub nor shared. Only their evaluation outputs are submitted
(see [Contributing](../contributing/index.md)).
