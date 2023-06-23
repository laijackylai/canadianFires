import pandas as pd
import glob
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from xgboost import plot_importance
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RandomizedSearchCV
import joblib

# data year: 1930-2021

# fire data index
# Index(['FID', 'SRC_AGENCY', 'FIRE_ID', 'FIRENAME', 'LATITUDE', 'LONGITUDE',
#        'YEAR', 'MONTH', 'DAY', 'REP_DATE', 'ATTK_DATE', 'OUT_DATE', 'DECADE',
#        'SIZE_HA', 'CAUSE', 'PROTZONE', 'FIRE_TYPE', 'MORE_INFO', 'CFS_REF_ID',
#        'CFS_NOTE1', 'CFS_NOTE2', 'ACQ_DATE', 'SRC_AGY2', 'ECOZONE', 'ECOZ_REF',
#        'ECOZ_NAME', 'ECOZ_NOM'],
#       dtype='object')

# temp data columns
# Index(['x', 'y', 'LATITUDE', 'LONGITUDE', 'STATION_NAME', 'CLIMATE_IDENTIFIER',
#        'ID', 'LOCAL_DATE', 'LAST_UPDATED', 'PROVINCE_CODE',
#        'ENG_PROVINCE_NAME', 'FRE_PROVINCE_NAME', 'LOCAL_YEAR', 'LOCAL_MONTH',
#        'NORMAL_MEAN_TEMPERATURE', 'MEAN_TEMPERATURE',
#        'DAYS_WITH_VALID_MEAN_TEMP', 'MIN_TEMPERATURE',
#        'DAYS_WITH_VALID_MIN_TEMP', 'MAX_TEMPERATURE',
#        'DAYS_WITH_VALID_MAX_TEMP', 'NORMAL_PRECIPITATION',
#        'TOTAL_PRECIPITATION', 'DAYS_WITH_VALID_PRECIP',
#        'DAYS_WITH_PRECIP_GE_1MM', 'NORMAL_SNOWFALL', 'TOTAL_SNOWFALL',
#        'DAYS_WITH_VALID_SNOWFALL', 'SNOW_ON_GROUND_LAST_DAY',
#        'NORMAL_SUNSHINE', 'BRIGHT_SUNSHINE', 'DAYS_WITH_VALID_SUNSHINE',
#        'COOLING_DEGREE_DAYS', 'HEATING_DEGREE_DAYS'],
#       dtype='object')


def read_fire_data():
    '''
    read fire data
    '''
    # Provide the fire file path
    file_path = './data/fire/NFDB_point_20220901.txt'

    # Read the CSV file into a DataFrame
    fire_df = pd.read_csv(file_path, delimiter=',')

    print('Read fire data')
    return fire_df[['FIRE_ID', 'SRC_AGENCY', 'YEAR', 'MONTH', 'CAUSE', 'SIZE_HA']]


def read_temp_data():
    '''
    read temperature data
    '''
    # Specify the directory where the CSV files are located
    directory = './data/temp/'

    # Get a list of all CSV file paths in the directory
    csv_files = glob.glob(directory + '*.csv')

    # Create an empty list to store the DataFrames
    dataframes = []

    # Read each CSV file and store it as a DataFrame
    for file in csv_files:
        df = pd.read_csv(file)
        dataframes.append(df)

    # Concatenate all DataFrames into a single DataFrame
    temp_df = pd.concat(dataframes, ignore_index=True)

    # drop empty entries where 'MEAN_TEMPERATURE' is empty
    temp_df.dropna(subset=['MEAN_TEMPERATURE'], inplace=True)

    print('Read temperature data')
    return temp_df[['ID', 'PROVINCE_CODE', 'LOCAL_YEAR', 'LOCAL_MONTH', 'MEAN_TEMPERATURE']]


def slice_training_data(data, year_index):
    '''
    slice training data from 1930-2000
    '''
    sliced_df = data[(data[year_index] >= 1930) & (data[year_index] < 2000)]
    return sliced_df


def slice_testing_data(data, year_index):
    '''
    slice testing data from 2000-2021
    '''
    sliced_df = data[(data[year_index] >= 2000) & (data[year_index] < 3000)]
    return sliced_df


def merge_data(f_data, t_data):
    '''merge the two datasets'''
    # Merge the two DataFrames based on the matching conditions
    m_data = t_data.merge(f_data, left_on=['PROVINCE_CODE', 'LOCAL_YEAR', 'LOCAL_MONTH'], right_on=[
        'SRC_AGENCY', 'YEAR', 'MONTH'], how='left')

    # Add the 'CAUSE' and 'SIZE_HA' columns to the merged DataFrame
    m_data['CAUSE'] = m_data['CAUSE'].fillna('')
    m_data['SIZE_HA'] = m_data['SIZE_HA'].fillna(0)

    m_data['CHANCE_OF_FIRE'] = m_data['SIZE_HA'].apply(
        lambda x: 1 if x > 0 else 0)

    print('Merged datasets')
    return m_data


if __name__ == "__main__":
    # Call the main function
    # * data cleaning
    fire_data = read_fire_data()
    temp_data = read_temp_data()

    merged_data = merge_data(fire_data, temp_data)
    merged_data = merged_data[['PROVINCE_CODE', 'LOCAL_YEAR', 'LOCAL_MONTH',
                               'MEAN_TEMPERATURE', 'CAUSE', 'SIZE_HA', 'CHANCE_OF_FIRE']]
    
    # limit province code to "ON" and drop that column
    merged_data = merged_data[merged_data['PROVINCE_CODE'] == 'ON']
    merged_data.drop('PROVINCE_CODE', axis=1, inplace=True)

    # Set default day value
    default_day = 1

    # Merge 'LOCAL_YEAR' and 'LOCAL_MONTH' into a single date column
    merged_data['DATE'] = pd.to_datetime(merged_data['LOCAL_YEAR'].astype(
        str) + '-' + merged_data['LOCAL_MONTH'].astype(str) + '-' + str(default_day))

    # Drop 'LOCAL_YEAR' and 'LOCAL_MONTH' columns
    merged_data.drop(['LOCAL_YEAR', 'LOCAL_MONTH'], axis=1, inplace=True)

    # Perform one-hot encoding on categorical columns
    merged_data = pd.get_dummies(merged_data, columns=['CAUSE'])
    # merged_data = pd.get_dummies(merged_data, columns=['PROVINCE_CODE'])

    # Split the data based on the year 2000
    train_data = merged_data[merged_data['DATE'] < '2000-01-01']
    test_data = merged_data[merged_data['DATE'] >= '2000-01-01']
    
    # Convert 'DATE' column to numeric type
    train_data['DATE'] = pd.to_numeric(train_data['DATE'])
    test_data['DATE'] = pd.to_numeric(test_data['DATE'])

    # Split the data into training and testing sets
    X_train = train_data.drop(['SIZE_HA', 'CHANCE_OF_FIRE'], axis=1)
    X_test = test_data.drop(['SIZE_HA', 'CHANCE_OF_FIRE'], axis=1)
    y_train = train_data[['SIZE_HA', 'CHANCE_OF_FIRE']]
    y_test = test_data[['SIZE_HA', 'CHANCE_OF_FIRE']]

    model = xgb.XGBRegressor(
        n_estimators=1000,
        nthread=5,
        max_depth=9,
        learning_rate=0.1,
        subsample=1.0,
        colsample_bytree=0.8,
        reg_alpha=0.5,
        reg_lambda=0,
        objective="reg:squarederror",
        eval_metric="mae"
    )

    # xgboost model eval metrics
    # “rmse” for root mean squared error.
    # “mae” for mean absolute error.
    # “logloss” for binary logarithmic loss and “mlogloss” for multi-class log loss(cross entropy).
    # “error” for classification error.
    # “auc” for area under ROC curve.

    # * Train the model
    model.fit(X_train, y_train,
                      eval_metric="mae",
                      eval_set=[(X_train, y_train),
                                (X_test, y_test)],
                      early_stopping_rounds=50,
                      verbose=False)

    # * Make predictions
    y_pred = model.predict(X_test)
    predictions = [np.round(value) for value in y_pred]

    # Evaluate the model (mean squared error for both SIZE_HA and CHANCE_OF_FIRE)
    mse_size_ha = mean_squared_error(
        y_test['SIZE_HA'], y_pred[:, 0])
    mse_chance_of_fire = mean_squared_error(
        y_test['CHANCE_OF_FIRE'], y_pred[:, 1])

    print("Mean Squared Error (SIZE_HA):", mse_size_ha)
    print("Mean Squared Error (CHANCE_OF_FIRE):",
          mse_chance_of_fire)
    
    joblib.dump(model, 'model.pkl')
    
    print('done')