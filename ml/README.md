# Machine Learning Part

## Descripton

This model currently supports predicting data in Ontario since only Ontario data have been trained

### Input

1. Canadian fires data from 1930 to 2021 with the following indexes

``` bash
['FID', 'SRC_AGENCY', 'FIRE_ID', 'FIRENAME', 'LATITUDE' 'LONGITUDE', 'YEAR', 'MONTH', 'DAY', 'REP_DATE', 'ATTK_DATE', 'OUT_DATE', 'DECADE', 'SIZE_HA', 'CAUSE', 'PROTZONE', 'FIRE_TYPE', 'MORE_INFO', 'CFS_REF_ID', 'CFS_NOTE1', 'CFS_NOTE2', 'ACQ_DATE', 'SRC_AGY2', 'ECOZONE', 'ECOZ_REF', 'ECOZ_NAME', 'ECOZ_NOM']
```

2. Ontario temperature data by month from 1930-2021 with the following indexes

``` bash
['x', 'y', 'LATITUDE', 'LONGITUDE', 'STATION_NAME' 'CLIMATE_IDENTIFIER', 'ID', 'LOCAL_DATE', 'LAST_UPDATED', 'PROVINCE_CODE', 'ENG_PROVINCE_NAME', 'FRE_PROVINCE_NAME', 'LOCAL_YEAR', 'LOCAL_MONTH', 'NORMAL_MEAN_TEMPERATURE', 'MEAN_TEMPERATURE', 'DAYS_WITH_VALID_MEAN_TEMP', 'MIN_TEMPERATURE', 'DAYS_WITH_VALID_MIN_TEMP', 'MAX_TEMPERATURE', 'DAYS_WITH_VALID_MAX_TEMP', 'NORMAL_PRECIPITATION', 'TOTAL_PRECIPITATION', 'DAYS_WITH_VALID_PRECIP', 'DAYS_WITH_PRECIP_GE_1MM', 'NORMAL_SNOWFALL', 'TOTAL_SNOWFALL', 'DAYS_WITH_VALID_SNOWFALL', 'SNOW_ON_GROUND_LAST_DAY', 'NORMAL_SUNSHINE', 'BRIGHT_SUNSHINE', 'DAYS_WITH_VALID_SUNSHINE', 'COOLING_DEGREE_DAYS', 'HEATING_DEGREE_DAYS']
```

3. The following inputs are extracted and parsed in for training, per province

``` bash
['DATE', 'MEAN_TEMPERATURE' 'CAUSE']
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
['SIZE_HA', 'CHANCE_OF_FIRE']
```

### Model Used

XGBoost Regression

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
