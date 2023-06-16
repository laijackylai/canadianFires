import pickle
import pandas as pd

with open('model_test.pkl', 'rb') as file:
    model = pickle.load(file)

keys = ['PROVINCE_CODE', 'MEAN_TEMPERATURE', 'DATE', 'CAUSE_', 'CAUSE_H', 'CAUSE_H-PB', 'CAUSE_L', 'CAUSE_U']
test_data = [
  {
    # 'PROVINCE_CODE': 'ON',
    'MEAN_TEMPERATURE': 32,
    'DATE': '2020-01-01',
    # 'CAUSE_': 0,
    # 'CAUSE_H': 1,
    # 'CAUSE_H-PB': 0,
    # 'CAUSE_L': 0,
    # 'CAUSE_U': 0
  }
]
df = pd.DataFrame(test_data)
df['DATE'] = pd.to_numeric(pd.to_datetime(df['DATE']))

predictions = model.predict(df)
print(predictions)
df_pred = pd.DataFrame(predictions, columns=["SIZE_HA", "CHANCE_OF_FIRE", "CAUSE_", "CAUSE_H", "CAUSE_H-PB", "CAUSE_L", "CAUSE_U"])

print(df_pred)