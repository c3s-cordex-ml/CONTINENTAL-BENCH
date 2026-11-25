# Experiments

There is one mandatory experiment and two optional ones. They differ only in the training data; all of them are tested on the
same test blocks (see [Predictions](predictions.md)). Training always uses **perfect** predictors.

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

## Validation years

The same four years are held out from the training blocks for validation (early stopping, model selection) in all experiments:
**1967, 1975, 2087 and 2095**. In experiment C they are held out from each of the three simulations.
