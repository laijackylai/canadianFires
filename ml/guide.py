#Import libraries:
import pandas as pd
import numpy as np
import xgboost as xgb
from xgboost.sklearn import XGBRegressor
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
import joblib
from sklearn.model_selection import train_test_split

rcParams['figure.figsize'] = 12, 4
fire_data = pd.read_csv('./data/fire/NFDB_point_20220901.csv')
target = ['SIZE_HA']
IDcol = ['FID', 'FIRE_ID']

def modelfit(alg, dtrain, target, predictors, useTrainCV=True, cv_folds=10, early_stopping_rounds=50):
    '''
    train and test the model
    '''
    if useTrainCV:
        xgb_param = alg.get_xgb_params()
        xgtrain = xgb.DMatrix(dtrain[predictors].values, label=target.values)
        cvresult = xgb.cv(
            xgb_param,
            xgtrain,
            num_boost_round=alg.get_params()['n_estimators'],
            nfold=cv_folds,
            metrics='rmse',  # Use 'rmse' for regression tasks
            early_stopping_rounds=early_stopping_rounds)
        alg.set_params(n_estimators=cvresult.shape[0])

    # Fit the algorithm on the data
    print('training model...')
    alg.fit(dtrain[predictors], target, eval_metric='rmse')

    # Predict testing set
    dtrain_predictions = alg.predict(X_test)

    # Print model report
    print("\nModel Report:")
    print("RMSE : %.4f" % np.sqrt(metrics.mean_squared_error(y_test, dtrain_predictions)))

    feat_imp = pd.Series(alg.feature_importances_, index=predictors).sort_values(ascending=False)
    feat_imp.plot(kind='bar', title='Feature Importances')
    plt.ylabel('Feature Importance Score')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility
    plt.show()

    model_filename = './models/optimized_xgb_regression_model.pkl'
    joblib.dump(alg, model_filename)
    print(f"Model saved to {model_filename}")

# filter SRC_AGENCY
df_filtered = fire_data[fire_data['SRC_AGENCY'].apply(len) <= 2]
# apply one hot encoding
one_hot_encoded_agency = pd.get_dummies(df_filtered['SRC_AGENCY'], prefix='SRC_AGENCY')
one_hot_encoded_cause = pd.get_dummies(df_filtered['CAUSE'], prefix='CAUSE')
new_train = pd.concat([df_filtered, one_hot_encoded_agency, one_hot_encoded_cause, ], axis=1)
final_train = new_train.drop(columns=['SRC_AGENCY', 'CAUSE'])

X = final_train.drop(columns=target + IDcol)  # Features (input variables)
y = final_train['SIZE_HA']
test_size = 0.2
random_state = 42
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

# Choose all predictors except target & IDcols
predictors = [x for x in final_train.columns if x not in target + IDcol]

xgb1 = XGBRegressor(
    learning_rate=0.01,
    n_estimators=5000,
    max_depth=2, # optimized
    min_child_weight=0, # optimized
    gamma=0, # optimized
    subsample=0.9, # optimized
    colsample_bytree=0.55, # optimized
    reg_alpha=99.5, # optimized
    nthread=8,
    seed=27)
modelfit(xgb1, X_train, y_train, predictors)

# * param test 1: max_depth, min_child_weight
# param_test1 = {
#     'max_depth': range(3, 10, 2),
#     'min_child_weight': range(1, 6, 2)
# }
# gsearch1 = GridSearchCV(
#     estimator=XGBRegressor(
#         learning_rate=0.1,
#         n_estimators=140,
#         max_depth=5,
#         min_child_weight=1,
#         gamma=0,
#         subsample=0.8,
#         colsample_bytree=0.8,
#         # nthread=4,
#         seed=27),
#     param_grid=param_test1,
#     scoring='neg_mean_squared_error',  # Use a regression metric like neg_mean_squared_error
#     n_jobs=8,
#     cv=5
# )
# gsearch1.fit(final_train[predictors], final_train[target])
# print("Grid search results:", gsearch1.cv_results_)
# print("Best parameters:", gsearch1.best_params_)
# print("Best negative RMSE score:", gsearch1.best_score_)
# best 3, 1

# * param test 2: narrow max_depth, min_child_weight
# param_test2 = {
#     'max_depth': [2, 3, 4],
#     'min_child_weight': [0, 1, 2]
# }
# gsearch2 = GridSearchCV(
#     estimator=XGBRegressor(
#         learning_rate=0.1,
#         n_estimators=140,
#         max_depth=5,
#         min_child_weight=1,
#         gamma=0,
#         subsample=0.8,
#         colsample_bytree=0.8,
#         # nthread=4,
#         seed=27),
#     param_grid=param_test2,
#     scoring='neg_mean_squared_error',  # Use a regression metric like neg_mean_squared_error
#     n_jobs=8,
#     cv=5
# )
# gsearch2.fit(final_train[predictors], final_train[target])
# print("Grid search results:", gsearch2.cv_results_)
# print("Best parameters:", gsearch2.best_params_)
# print("Best negative RMSE score:", gsearch2.best_score_)
# best max_depth 2, min_child_weight 0

# * param test 3: narrower min_child_weight
# param_test3 = {
#     'min_child_weight': [-2, -1, 0]
# }
# gsearch3 = GridSearchCV(
#     estimator=XGBRegressor(
#         learning_rate=0.1,
#         n_estimators=140,
#         max_depth=5,
#         min_child_weight=1,
#         gamma=0,
#         subsample=0.8,
#         colsample_bytree=0.8,
#         # nthread=4,
#         seed=27),
#     param_grid=param_test3,
#     scoring='neg_mean_squared_error',  # Use a regression metric like neg_mean_squared_error
#     n_jobs=8,
#     cv=5
# )
# gsearch3.fit(final_train[predictors], final_train[target])
# print("Grid search results:", gsearch3.cv_results_)
# print("Best parameters:", gsearch3.best_params_)
# print("Best negative RMSE score:", gsearch3.best_score_)
# best min_child_weight 0

# * param test 4: gamma
# param_test4 = {
#     'gamma': [i/10.0 for i in range(0,5)]
# }
# gsearch4 = GridSearchCV(
#     estimator=XGBRegressor(
#         learning_rate=0.1,
#         n_estimators=140,
#         max_depth=5,
#         min_child_weight=1,
#         gamma=0,
#         subsample=0.8,
#         colsample_bytree=0.8,
#         # nthread=4,
#         seed=27),
#     param_grid=param_test4,
#     scoring='neg_mean_squared_error',  # Use a regression metric like neg_mean_squared_error
#     n_jobs=8,
#     cv=5
# )
# gsearch4.fit(final_train[predictors], final_train[target])
# print("Grid search results:", gsearch4.cv_results_)
# print("Best parameters:", gsearch4.best_params_)
# print("Best negative RMSE score:", gsearch4.best_score_)
# best gamma 0

# * param test 5: subsample, colsample_bytree
# param_test5 = {
#     'subsample':[i/10.0 for i in range(6,10)],
#     'colsample_bytree':[i/10.0 for i in range(6,10)]
# }
# gsearch5 = GridSearchCV(
#     estimator=XGBRegressor(
#         learning_rate=0.1,
#         n_estimators=140,
#         max_depth=5,
#         min_child_weight=1,
#         gamma=0,
#         subsample=0.8,
#         colsample_bytree=0.8,
#         # nthread=4,
#         seed=27),
#     param_grid=param_test5,
#     scoring='neg_mean_squared_error',  # Use a regression metric like neg_mean_squared_error
#     n_jobs=8,
#     cv=5
# )
# gsearch5.fit(final_train[predictors], final_train[target])
# print("Grid search results:", gsearch5.cv_results_)
# print("Best parameters:", gsearch5.best_params_)
# print("Best negative RMSE score:", gsearch5.best_score_)
# best subsample 0.6, colsample_bytree 0.9

# * param test 6: narrow subsample, colsample_bytree
# param_test6 = {
#     'subsample':[i/100.0 for i in range(55, 65, 5)],
#     'colsample_bytree':[i/100.0 for i in range(85, 95, 5)]
# }
# gsearch6 = GridSearchCV(
#     estimator=XGBRegressor(
#         learning_rate=0.1,
#         n_estimators=140,
#         max_depth=5,
#         min_child_weight=1,
#         gamma=0,
#         subsample=0.8,
#         colsample_bytree=0.8,
#         # nthread=4,
#         seed=27),
#     param_grid=param_test6,
#     scoring='neg_mean_squared_error',  # Use a regression metric like neg_mean_squared_error
#     n_jobs=8,
#     cv=5
# ) 
# gsearch6.fit(final_train[predictors], final_train[target])
# print("Grid search results:", gsearch6.cv_results_)
# print("Best parameters:", gsearch6.best_params_)
# print("Best negative RMSE score:", gsearch6.best_score_)
# best subsample 0.9, colsample_bytree 0.55

# * param test 7: reg_alpha
# param_test7 = {
#     'reg_alpha':[1e-5, 1e-2, 0.1, 1, 100]
# }
# gsearch7 = GridSearchCV(
#     estimator=XGBRegressor(
#         learning_rate=0.1,
#         n_estimators=140,
#         max_depth=5,
#         min_child_weight=1,
#         gamma=0,
#         subsample=0.8,
#         colsample_bytree=0.8,
#         # nthread=4,
#         seed=27),
#     param_grid=param_test7,
#     scoring='neg_mean_squared_error',  # Use a regression metric like neg_mean_squared_error
#     n_jobs=8,
#     cv=5
# ) 
# gsearch7.fit(final_train[predictors], final_train[target])
# print("Grid search results:", gsearch7.cv_results_)
# print("Best parameters:", gsearch7.best_params_)
# print("Best negative RMSE score:", gsearch7.best_score_)
# best reg_alpha 100

# * param test 8: narrow reg_alpha
# param_test8 = {
#     'reg_alpha':[i for i in range(80, 100, 5)]
# }
# gsearch8 = GridSearchCV(
#     estimator=XGBRegressor(
#         learning_rate=0.1,
#         n_estimators=140,
#         max_depth=5,
#         min_child_weight=1,
#         gamma=0,
#         subsample=0.8,
#         colsample_bytree=0.8,
#         # nthread=4,
#         seed=27),
#     param_grid=param_test8,
#     scoring='neg_mean_squared_error',  # Use a regression metric like neg_mean_squared_error
#     n_jobs=8,
#     cv=5
# ) 
# gsearch8.fit(final_train[predictors], final_train[target])
# print("Grid search results:", gsearch8.cv_results_)
# print("Best parameters:", gsearch8.best_params_)
# print("Best negative RMSE score:", gsearch8.best_score_)
# best reg_alpha 95

# * param test 9: narrow reg_alpha
# param_test9 = {
#     'reg_alpha':[i for i in range(90, 100)]
# }
# gsearch9 = GridSearchCV(
#     estimator=XGBRegressor(
#         learning_rate=0.1,
#         n_estimators=140,
#         max_depth=5,
#         min_child_weight=1,
#         gamma=0,
#         subsample=0.8,
#         colsample_bytree=0.8,
#         # nthread=4,
#         seed=27),
#     param_grid=param_test9,
#     scoring='neg_mean_squared_error',  # Use a regression metric like neg_mean_squared_error
#     n_jobs=8,
#     cv=5
# ) 
# gsearch9.fit(final_train[predictors], final_train[target])
# print("Grid search results:", gsearch9.cv_results_)
# print("Best parameters:", gsearch9.best_params_)
# print("Best negative RMSE score:", gsearch9.best_score_)
# best reg_alpha 99

# * param test 10: narrow reg_alpha
# param_test9 = {
#     'reg_alpha':[98.2, 98.4, 98.6, 98.8, 99, 99.2, 99.4, 99.6, 99.8]
# }
# gsearch9 = GridSearchCV(
#     estimator=XGBRegressor(
#         learning_rate=0.1,
#         n_estimators=140,
#         max_depth=5,
#         min_child_weight=1,
#         gamma=0,
#         subsample=0.8,
#         colsample_bytree=0.8,
#         # nthread=4,
#         seed=27),
#     param_grid=param_test9,
#     scoring='neg_mean_squared_error',  # Use a regression metric like neg_mean_squared_error
#     n_jobs=8,
#     cv=5
# ) 
# gsearch9.fit(final_train[predictors], final_train[target])
# print("Grid search results:", gsearch9.cv_results_)
# print("Best parameters:", gsearch9.best_params_)
# print("Best negative RMSE score:", gsearch9.best_score_)
# best reg_alpha 99.8