# Machine Learning Part

## Descripton

This model currently supports predicting data in Ontario since only Ontario data have been trained

### Input

1. Canadian fires data from 1930 to 2021 with the following indexes

| Field | Name Description |
| ----- | ---------------- |
FID | Internal feature number.
Shape | Feature geometry.
SRC_AGENCY | Agency (province, territory, parks) from which the fire data has been obtained.
YEAR | Year of fire as provided by individual agencies.
FIRE_ID | Agency fire ID.
FIRENAME | Agency firename.
LATITUDE | Latitude.
LONGITUDE | Longitude.
MONTH | Month of fire as provided by individual agencies.
DAY Day | of fire as provided by individual agencies.
REP_DATE | Date associated with fire as reported by individual agency.
SIZE_HA | Fire size (hectares) as reported by agency.
ATTK_DATE | Date when fire attack occurred.
OUT_DATE | Date agency indicates fire is out or extinguished.
CAUSE | Cause of fire as reported by agency.
PROTZONE | Protection Zone as indicated by source agency.
FIRE_TYPE | Fire type as indicated by source agency.
MORE_INFO | Additional attributes provided by agency.
CFS_REF_ID | Fire reference ID.
ACQ_DATE | Date that fire data was acquired from agency.
CFS_NOTE1 | Additional note added by CFS when compiling the NFDB.
CFS_NOTE2 | Additional note added by CFS when compiling the NFDB.
DECADE | Decade.
ECOZONE | Ecodistrict associated with fire point location.
SRC_AGY2 | Source agency 2.
ECOZ_REF | Ecozone reference ID associated with fire point location.
ECOZ_NAME | Ecozone name associated with fire point location.
ECOZ_NOM | Ecozone name (FR) associated with fire point location.

2. Ontario temperature data by month from 1930-2021 with the following indexes

``` bash
['x', 'y', 'LATITUDE', 'LONGITUDE', 'STATION_NAME' 'CLIMATE_IDENTIFIER', 'ID', 'LOCAL_DATE', 'LAST_UPDATED', 'PROVINCE_CODE', 'ENG_PROVINCE_NAME', 'FRE_PROVINCE_NAME', 'LOCAL_YEAR', 'LOCAL_MONTH', 'NORMAL_MEAN_TEMPERATURE', 'MEAN_TEMPERATURE', 'DAYS_WITH_VALID_MEAN_TEMP', 'MIN_TEMPERATURE', 'DAYS_WITH_VALID_MIN_TEMP', 'MAX_TEMPERATURE', 'DAYS_WITH_VALID_MAX_TEMP', 'NORMAL_PRECIPITATION', 'TOTAL_PRECIPITATION', 'DAYS_WITH_VALID_PRECIP', 'DAYS_WITH_PRECIP_GE_1MM', 'NORMAL_SNOWFALL', 'TOTAL_SNOWFALL', 'DAYS_WITH_VALID_SNOWFALL', 'SNOW_ON_GROUND_LAST_DAY', 'NORMAL_SUNSHINE', 'BRIGHT_SUNSHINE', 'DAYS_WITH_VALID_SUNSHINE', 'COOLING_DEGREE_DAYS', 'HEATING_DEGREE_DAYS']
```

3. The following inputs are extracted and parsed in for training, per province

``` bash
['LAT', 'LON', 'YEAR', 'MONTH', 'DAY', 'MEAN_TEMPERATURE', 'MEAN_PRECIPITATON', 'MEAN_SNOWFALL']
```

Breaking down the causes:

- U: Unknown cause
- L: Lightning casued fire
- H: Human caused fire
- H-PB: Prescribed burn (human caused)
- Re: Reburn. examine for original cause

Monthly Mean Temperature are provided

### Output

The resulted output of the model will be the following two variables

``` bash
['SIZE_HA', 'CAUSE']
```

### Model Used

XGBoost Regression

#### Strengths

- Exceptional predictive accuracy
- Handles complex relationships and non-linear patterns effectively
- Regularization techniques (L1, L2) mitigate overfitting
- Capable of handling missing values
- Provides feature importance ranking
- Supports parallel processing for scalability
- Can handle large-scale datasets efficiently
- Flexible and customizable through hyperparameter tuning
- Suitable for both regression and classification tasks

#### Weaknesses

- Computationally expensive for large datasets or complex models
- Sensitivity to hyperparameters, requiring careful tuning
- Susceptible to overfitting without proper regularization and tuning
- Less interpretable compared to simpler models
- Limited performance on small datasets

#### How does the model work

1. Initialize the Model: Initially, XGBoost regression sets the predicted values to a constant value, typically the mean of the target variable. This serves as the starting point for subsequent iterations.

2. Calculate Residuals: The residuals are the differences between the actual target values and the current predicted values. These residuals represent the errors made by the model in the previous iteration.

3. Build a Regression Tree: XGBoost regression constructs a decision tree to model the residuals. The decision tree is built by recursively splitting the data based on the features, aiming to reduce the residuals in each leaf node. The tree structure and split points are determined using a greedy algorithm that maximizes the reduction in the loss function.

4. Compute the Tree's Weight: After the tree is built, a weight (also called the learning rate or shrinkage factor) is assigned to the tree. This weight determines the contribution of the tree's predictions to the final model. Initially, all trees have equal weights.

5. Update Predictions: The predictions from the newly constructed tree are combined with the previous predictions by adding them in a weighted manner. The weights are determined by the learning rate.

6. Calculate the New Residuals: The residuals are recalculated using the updated predictions. These new residuals represent the errors that remain after incorporating the predictions from the latest tree.

7. Repeat Steps 3-6: Steps 3 to 6 are repeated iteratively for a specified number of boosting rounds. In each iteration, a new tree is built to model the remaining residuals, and the predictions and residuals are updated accordingly.

8. Regularization: To prevent overfitting, XGBoost regression applies regularization techniques. Two common regularization methods are L1 (Lasso) and L2 (Ridge) regularization. These techniques introduce penalties to the objective function, discouraging complex models and promoting simpler solutions.

9. Finalize the Model: After the specified number of boosting rounds is reached, or when a stopping criterion is met, XGBoost regression finalizes the model. The final prediction is the sum of predictions from all the constructed trees, each weighted by the learning rate.

### How can XGBoost be ran in parallel

XGBoost can be parallelized in multiple ways:

- Parallelization within a tree: Operations like evaluating splitting points can be done in parallel within a single tree.
- Parallelization across trees: Multiple trees can be built independently in parallel since they don't depend on each other's results.
- Column subsampling: XGBoost supports feature subsampling, allowing different subsets of features to be processed independently in parallel.

### Best Params

| Param            | Value | Description |
| ---------------- | ----- | ----------- |
| n_estimators     | 200   | The number of boosting rounds or decision trees to be built. Higher values may improve model performance but can also increase training time and resource requirements. |
| subsample        | 1.0   | The fraction of samples to be randomly selected for each tree. A value of 1.0 means that all samples are used. Setting it to a lower value can help prevent overfitting by introducing randomness in the training process.
| reg_lambda       | 0     | L2 regularization term for the weights. It helps to control the complexity of the model by penalizing large weights. A value of 0 means no regularization is applied. |
| reg_alpha        | 0.5   | L1 regularization term for the weights. It encourages sparsity in feature selection by pushing some weights to exactly zero. A non-zero value introduces regularization. |
| max_depth        | 9     | The maximum depth of each decision tree in the ensemble. Increasing this value can allow the model to capture more complex relationships in the data but may also lead to overfitting. |
| learning_rate    | 0.1   | The learning rate or step size for each boosting round. It scales the contribution of each tree in the ensemble. A smaller value requires more trees for model convergence but can help improve generalization. |
| colsample_bytree | 0.8   | The fraction of features (columns) to be randomly selected for each tree. A value of 1.0 means that all features are used. Setting it to a lower value can help introduce diversity and reduce the risk of overfitting. |

Mean Squared Error (SIZE_HA): 6982052.993950239
Mean Squared Error (CHANCE_OF_FIRE): 0.18242572046681263

MSE of SIZE_HA:

- Many outlier data in the size of fires
- many small fires but some huge ones here and there
- also seems no corelation of size of fire to the cause and temperature
