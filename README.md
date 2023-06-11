# TempHuFire

## Descripton

This is an attempt to use Machine Learning to corelate and predict Canadian fires with temperature and humidity

### Input

1. Canadian fires data from 1930 to 2021 with the following indexes

``` bash
['FID', 'SRC_AGENCY', 'FIRE_ID', 'FIRENAME', 'LATITUDE' 'LONGITUDE', 'YEAR', 'MONTH', 'DAY', 'REP_DATE', 'ATTK_DATE', 'OUT_DATE', 'DECADE', 'SIZE_HA', 'CAUSE', 'PROTZONE', 'FIRE_TYPE', 'MORE_INFO', 'CFS_REF_ID', 'CFS_NOTE1', 'CFS_NOTE2', 'ACQ_DATE', 'SRC_AGY2', 'ECOZONE', 'ECOZ_REF', 'ECOZ_NAME', 'ECOZ_NOM']
```

2. Canadian temperature data by month from 1930-2021 with the following indexes

``` bash
['x', 'y', 'LATITUDE', 'LONGITUDE', 'STATION_NAME' 'CLIMATE_IDENTIFIER', 'ID', 'LOCAL_DATE', 'LAST_UPDATED', 'PROVINCE_CODE', 'ENG_PROVINCE_NAME', 'FRE_PROVINCE_NAME', 'LOCAL_YEAR', 'LOCAL_MONTH', 'NORMAL_MEAN_TEMPERATURE', 'MEAN_TEMPERATURE', 'DAYS_WITH_VALID_MEAN_TEMP', 'MIN_TEMPERATURE', 'DAYS_WITH_VALID_MIN_TEMP', 'MAX_TEMPERATURE', 'DAYS_WITH_VALID_MAX_TEMP', 'NORMAL_PRECIPITATION', 'TOTAL_PRECIPITATION', 'DAYS_WITH_VALID_PRECIP', 'DAYS_WITH_PRECIP_GE_1MM', 'NORMAL_SNOWFALL', 'TOTAL_SNOWFALL', 'DAYS_WITH_VALID_SNOWFALL', 'SNOW_ON_GROUND_LAST_DAY', 'NORMAL_SUNSHINE', 'BRIGHT_SUNSHINE', 'DAYS_WITH_VALID_SUNSHINE', 'COOLING_DEGREE_DAYS', 'HEATING_DEGREE_DAYS']
```

3. The following inputs are extracted and parsed in for training, per province

``` bash
['LOCAL_YEAR', 'LOCAL_MONTH', 'MEAN_TEMPERATURE' 'CAUSE']
```

### Output

The resulted output of the model will be the following two variables

``` bash
['SIZE_HA', 'CHANCE_OF_FIRE']
```
