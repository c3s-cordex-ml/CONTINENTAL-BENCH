# CONTINENTAL-BENCH

CONTINENTAL-BENCH is a benchmark of machine-learning emulators of a regional climate model over Europe.
The emulators learn to reproduce the daily output of **RegCM5-0** on the **EURO-CORDEX EUR-12** domain (CORDEX-CORE-CMIP6)
from coarse-resolution upper-air predictors, and are tested on how well they reproduce both the present climate and the
climate-change signal under SSP3-7.0.

It is developed within the Copernicus Climate Change Service contract **C3S2_384**. Each partner of the consortium trains its
own emulator on the same data and evaluates it with the same tools, so that the results are directly comparable.

!!! warning "Under development"
    The experimental protocol is still being finalised. Sections marked *TBD* will be completed as decisions are made.

## Contents

- [Introduction](introduction/index.md): the data, the experiments, the predictions every model must produce and how they are evaluated.
- [Contributing](contributing/index.md): how to download the data, train a model, prepare and evaluate its predictions, and submit the evaluation outputs.
- [Results](results/index.md): scoreboards and the validation portal.

## Contact

Questions and suggestions are welcome as GitHub issues in this repository.
