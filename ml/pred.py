import pickle
import pandas as pd

with open('best_cause_model.pkl', 'rb') as file:
    model = pickle.load(file)

test_data = [
  {
    'LATITUDE': 48.67589427, 
    'LONGITUDE': -89.89406998,
    'YEAR': 2020,
    'MONTH': 5,
    'DAY': 13,
    'ECOZONE': 15, # either 0, 6, 8, 15
    # 'PROVINCE_CODE': 'ON',
    'MEAN_TEMPERATURE': 30,
    'MEAN_PRECIPITATION': 0,
    'MEAN_SNOWFALL': 0,
    # 'CAUSE_': 0,
    # 'CAUSE_H': 1,
    # 'CAUSE_H-PB': 0,
    # 'CAUSE_L': 0,
    # 'CAUSE_U': 0
  }
]

df = pd.DataFrame(test_data)
# df['DATE'] = pd.to_numeric(pd.to_datetime(df['DATE']))

predictions = model.predict(df)
# print(predictions)

df_pred = pd.DataFrame(predictions, columns=['SIZE_HA', 'CAUSE_H','CAUSE_H-PB', 'CAUSE_L', 'CAUSE_U', 'FIRE_TYPE_Fire', 'FIRE_TYPE_IFR', 'FIRE_TYPE_OFR', 'FIRE_TYPE_PB', 'FIRE_TYPE_Prescribed Burn'])
print(df_pred)

cause_name = df_pred[['CAUSE_H', 'CAUSE_H-PB', 'CAUSE_L', 'CAUSE_U']].max().idxmax()
fire_type_name = df_pred[['FIRE_TYPE_Fire', 'FIRE_TYPE_IFR', 'FIRE_TYPE_OFR', 'FIRE_TYPE_PB', 'FIRE_TYPE_Prescribed Burn']].max().idxmax()

print('Fire size: ', df_pred['SIZE_HA'][0])
print('Cause: ', cause_name)
print('Fire type: ', fire_type_name)
