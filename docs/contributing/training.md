# Train your model

Train your model on the **perfect** predictors and the targets of the training blocks of each experiment (see
[Experiments](../introduction/experiments.md)). 

Things to keep in mind:

- Cells outside the RegCM5-0 domain are NaN in the perfect predictors. Your model must handle them, e.g. by setting them to zero
  after normalisation; at inference, apply the same mask to the imperfect predictors.
- Hold out the validation years 1967, 1975, 2087 and 2095 (see [Experiments](../introduction/experiments.md)).

