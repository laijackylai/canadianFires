import math
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
from scipy.spatial.distance import cdist

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
    
    # * filter Ontario data
    fire_df = fire_df[fire_df['SRC_AGENCY'] == 'ON']
    
    fire_df['FIRE_TYPE'] = fire_df['FIRE_TYPE'].fillna('Fire').replace(' ', 'Fire').replace('', 'Fire')
    
    # drop rows where MONTH is 0
    fire_df = fire_df.drop(fire_df[fire_df['MONTH'] == 0].index)
    
    print('Read fire data')
    return fire_df[['LATITUDE', 'LONGITUDE',
       'YEAR', 'MONTH', 'DAY', 'SIZE_HA', 'CAUSE', 
       'FIRE_TYPE', 'ECOZONE']]


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
    
    temp_df['MEAN_PRECIPITATION'] = temp_df['TOTAL_PRECIPITATION'] / 30.437
    temp_df['MEAN_SNOWFALL'] = temp_df['TOTAL_SNOWFALL'] / temp_df['DAYS_WITH_VALID_SNOWFALL']
    
    print('Read temperature data')
    return temp_df[['LATITUDE', 'LONGITUDE', 'LOCAL_YEAR', 'LOCAL_MONTH', 'MEAN_TEMPERATURE', 'MEAN_PRECIPITATION', 'MEAN_SNOWFALL']]


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

def euclidean_distance(point1, point2):
    '''
    calculate euclidean distance
    '''
    squared_sum = 0
    for i in range(len(point1)):
        squared_sum += (point1[i] - point2[i]) ** 2
    distance = math.sqrt(squared_sum)
    return distance

def merge_data(f_data, t_data):
    '''merge the two datasets'''
    
    for index, row1 in f_data.iterrows():
        year = row1['YEAR']
        month = row1['MONTH']
                
        filtered_t_data = t_data[(t_data['LOCAL_YEAR'] == year) & (t_data['LOCAL_MONTH'] == month)]

        min_distance = float('inf')
        closest_row = None
        for _, row2 in filtered_t_data.iterrows():
            distance = euclidean_distance([row1['LATITUDE'], row1['LONGITUDE']],
                                        [row2['LATITUDE'], row2['LONGITUDE']])
            if distance < min_distance:
                min_distance = distance
                closest_row = row2
            
        if closest_row is not None:
            f_data.at[index, 'MEAN_TEMPERATURE'] = closest_row['MEAN_TEMPERATURE']
            f_data.at[index, 'MEAN_PRECIPITATION'] = closest_row['MEAN_PRECIPITATION']
            f_data.at[index, 'MEAN_SNOWFALL'] = closest_row['MEAN_SNOWFALL']
        else:
            print(row1)
            f_data.at[index, 'MEAN_TEMPERATURE'] = np.nan
            f_data.at[index, 'MEAN_PRECIPITATION'] = np.nan
            f_data.at[index, 'MEAN_SNOWFALL'] = np.nan
                                    
    return f_data


if __name__ == "__main__":
    # Call the main function
    # * data cleaning
    # fire_data = read_fire_data()
    # temp_data = read_temp_data()
    
    # merge fire and temp data
    # merged_data = merge_data(fire_data, temp_data)
        
    # merged_data = merged_data[['PROVINCE_CODE', 'LOCAL_YEAR', 'LOCAL_MONTH',
    #                            'MEAN_TEMPERATURE', 'CAUSE', 'SIZE_HA', 'CHANCE_OF_FIRE']]
    
    # limit province code to "ON" and drop that column
    # merged_data = merged_data[merged_data['PROVINCE_CODE'] == 'ON']
    # merged_data.drop('PROVINCE_CODE', axis=1, inplace=True)

    # Set default day value
    # default_day = 1

    # Merge 'LOCAL_YEAR' and 'LOCAL_MONTH' into a single date column
    # merged_data['DATE'] = pd.to_datetime(merged_data['LOCAL_YEAR'].astype(
    #     str) + '-' + merged_data['LOCAL_MONTH'].astype(str) + '-' + str(default_day))

    # Drop 'LOCAL_YEAR' and 'LOCAL_MONTH' columns
    # merged_data.drop(['LOCAL_YEAR', 'LOCAL_MONTH'], axis=1, inplace=True)

    # Perform one-hot encoding on categorical columns
    # merged_data = pd.get_dummies(merged_data, columns=['CAUSE'])
    # merged_data = pd.get_dummies(merged_data, columns=['FIRE_TYPE'])
    
    # merged_data.to_csv('merged_data.csv', index=False)
    
    # data columns: ['LATITUDE', 'LONGITUDE', 'YEAR', 'MONTH', 'DAY', 'SIZE_HA', 'ECOZONE',
    #    'MEAN_TEMPERATURE', 'MEAN_PRECIPITATION', 'MEAN_SNOWFALL', 'CAUSE_H',
    #    'CAUSE_H-PB', 'CAUSE_L', 'CAUSE_U', 'FIRE_TYPE_Fire', 'FIRE_TYPE_IFR',
    #    'FIRE_TYPE_OFR', 'FIRE_TYPE_PB', 'FIRE_TYPE_Prescribed Burn']
    
    merged_data = pd.read_csv('./merged_data.csv', delimiter=',')
    
    # Split the data based on the year 2000
    train_data = merged_data[merged_data['YEAR'] < 2000]
    test_data = merged_data[merged_data['YEAR'] >= 2000]
    
    # Convert 'DATE' column to numeric type
    # train_data['DATE'] = pd.to_numeric(train_data['DATE'])
    # test_data['DATE'] = pd.to_numeric(test_data['DATE'])

    # Split the data into training and testing sets
    X_train = train_data.drop(['SIZE_HA', 'CAUSE_H','CAUSE_H-PB', 'CAUSE_L', 'CAUSE_U', 'FIRE_TYPE_Fire', 'FIRE_TYPE_IFR', 'FIRE_TYPE_OFR', 'FIRE_TYPE_PB', 'FIRE_TYPE_Prescribed Burn'], axis=1)
    X_test = test_data.drop(['SIZE_HA', 'CAUSE_H','CAUSE_H-PB', 'CAUSE_L', 'CAUSE_U', 'FIRE_TYPE_Fire', 'FIRE_TYPE_IFR', 'FIRE_TYPE_OFR', 'FIRE_TYPE_PB', 'FIRE_TYPE_Prescribed Burn'], axis=1)
    y_train = train_data[['SIZE_HA', 'CAUSE_H','CAUSE_H-PB', 'CAUSE_L', 'CAUSE_U', 'FIRE_TYPE_Fire', 'FIRE_TYPE_IFR', 'FIRE_TYPE_OFR', 'FIRE_TYPE_PB', 'FIRE_TYPE_Prescribed Burn']]
    y_test = test_data[['SIZE_HA', 'CAUSE_H','CAUSE_H-PB', 'CAUSE_L', 'CAUSE_U', 'FIRE_TYPE_Fire', 'FIRE_TYPE_IFR', 'FIRE_TYPE_OFR', 'FIRE_TYPE_PB', 'FIRE_TYPE_Prescribed Burn']]
    
    # # * test parameters
    # param_space = {
    #     "max_depth": [10, 20, 30, 40],
    #     "learning_rate": [0.1, 0.2],
    #     "subsample": [0.5, 0.8, 1.0],
    #     "colsample_bytree": [0.8, 1.0],
    #     "reg_alpha": [0, 0.5, 1],
    #     "reg_lambda": [0, 0.5, 1]
    # }

    # # Define the number of iterations
    # num_iterations = 100

    # # * Define the XGBoost regressor
    # model = xgb.XGBRegressor(n_jobs=8)

    # # Perform Random Search
    # random_search = RandomizedSearchCV(
    #     estimator=model,
    #     param_distributions=param_space,
    #     n_iter=num_iterations,
    #     scoring='neg_mean_squared_error',
    #     cv=5,
    #     verbose=1,
    #     random_state=42
    # )
    
    # # * Train the model
    # random_search.fit(X_train, y_train,
    #                   eval_metric="rmse",
    #                   eval_set=[(X_train, y_train),
    #                             (X_test, y_test)],
    #                   early_stopping_rounds=50,
    #                   verbose=False)

    # best_params = random_search.best_params_
    # best_model = random_search.best_estimator_
    
    # print(best_params)
    # print(best_model)
    
    # {'subsample': 0.8, 'reg_lambda': 1, 'reg_alpha': 1, 'max_depth': 10, 'learning_rate': 0.1, 'colsample_bytree': 0.8}
    model = xgb.XGBRegressor(n_estimators=200,
                             n_jobs=8,
                             max_depth=10,
                             learning_rate=0.1,
                             subsample=0.8,
                             colsample_bytree=0.8,
                             reg_alpha=1,
                             reg_lambda=1,
                             objective="reg:squarederror")

    # xgboost model eval metrics
    # “rmse” for root mean squared error.
    # “mae” for mean absolute error.
    # “logloss” for binary logarithmic loss and “mlogloss” for multi-class log loss(cross entropy).
    # “error” for classification error.
    # “auc” for area under ROC curve.

    # * Train the model
    model.fit(X_train, y_train,
                      eval_metric="rmse",
                      eval_set=[(X_train, y_train),
                                (X_test, y_test)],
                      early_stopping_rounds=50,
                      verbose=False)
    
    # * plot feature importance
    xgb.plot_importance(model)
    plt.show()

    # * Make predictions
    y_pred = model.predict(X_test)
    predictions = [np.round(value) for value in y_pred]

    mse_size_ha = mean_squared_error(y_test['SIZE_HA'], y_pred[:, 0])
    print("MSE for SIZE_HA:", mse_size_ha)
    mse_cause_h = mean_squared_error(y_test['CAUSE_H'], y_pred[:, 1])
    print("MSE for CAUSE_H:", mse_cause_h)
    mse_cause_h_pb = mean_squared_error(y_test['CAUSE_H-PB'], y_pred[:, 2])
    print("MSE for CAUSE_H-PB:", mse_cause_h_pb)
    mse_cause_l = mean_squared_error(y_test['CAUSE_L'], y_pred[:, 3])
    print("MSE for CAUSE_L:", mse_cause_l)
    mse_cause_u = mean_squared_error(y_test['CAUSE_U'], y_pred[:, 4])
    print("MSE for CAUSE_U:", mse_cause_u)
    mse_fire_type_fire = mean_squared_error(y_test['FIRE_TYPE_Fire'], y_pred[:, 5])
    print("MSE for FIRE_TYPE_Fire:", mse_fire_type_fire)
    mse_fire_type_ifr = mean_squared_error(y_test['FIRE_TYPE_IFR'], y_pred[:, 6])
    print("MSE for FIRE_TYPE_IFR:", mse_fire_type_ifr)
    mse_fire_type_ofr = mean_squared_error(y_test['FIRE_TYPE_OFR'], y_pred[:, 7])
    print("MSE for FIRE_TYPE_OFR:", mse_fire_type_ofr)
    mse_fire_type_pb = mean_squared_error(y_test['FIRE_TYPE_PB'], y_pred[:, 8])
    print("MSE for FIRE_TYPE_PB:", mse_fire_type_pb)
    mse_fire_type_prescribed_burn = mean_squared_error(y_test['FIRE_TYPE_Prescribed Burn'], y_pred[:, 9])
    print("MSE for FIRE_TYPE_Prescribed Burn:", mse_fire_type_prescribed_burn)
    
    joblib.dump(model, 'best_cause_model.pkl')
    print('done')