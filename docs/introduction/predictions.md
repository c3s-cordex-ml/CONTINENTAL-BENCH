# Predictions

Every model trained in an experiment is applied to the same **test blocks**, with perfect and, where available, imperfect
predictors:

| Test | Block | Perfect | Imperfect |
|---|---|---|---|
| Historical | EC-Earth3-Veg/1981-2000 | ✔ | *pending* |
| | MPI-ESM1-2-HR/1981-2000 | ✔ | ✔ |
| | NorESM2-MM/1981-2000 | ✔ | ✔ |
| Mid-century | EC-Earth3-Veg/2041-2060 | <span class="skill">✔</span> | ✔ |
| | MPI-ESM1-2-HR/2041-2060 | ✔ | ✔ |
| | NorESM2-MM/2041-2060 | ✔ | ✔ |
| Evaluation | ERA5/1981-2000 | <span class="skill">✔</span> | <span class="skill">✔</span> |

*Test blocks to predict with each model, by type of predictors. Blue <span class="skill">✔</span>: predictions evaluated for
skill; black ✔: predictions used for the climate-change signal only.*

That is 13 predictions per model and experiment (14 once the EC-Earth3-Veg historical imperfect predictors are available),
each covering the 11 target variables.

Together they serve three purposes:

- **Skill** against the RegCM5-0 truth, with perfect predictors (EC-Earth3-Veg 2041-2060 and ERA5 1981-2000).
- **Skill against observations**, with ERA5 as imperfect predictor and ERA5-Land as reference.
- **Climate-change signal** (2041-2060 minus 1981-2000) for each GCM, which gives an ensemble of three perfect and, for now,
  two imperfect members.

Predictions stay at each centre: they are neither uploaded to GitHub nor shared. Only their evaluation outputs are submitted
(see [Contributing](../contributing/index.md)).
