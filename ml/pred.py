import pickle
import sqlite3
import pandas as pd
import argparse

def causeMap(c):
    '''
    cause map
    '''
    if c == 'CAUSE_H':
        return 'Humans'
    elif c == 'CAUSE_H-PB':
        return 'Prescribed burn (human caused)'
    elif c == 'CAUSE_L':
        return 'Lightning'
    elif c == 'CAUSE_U':
        return 'Unknown'

parser = argparse.ArgumentParser()
parser.add_argument("--lat", help="lat", required=True)
parser.add_argument("--lon", help="lon", required=True)
parser.add_argument("--year", help="year", required=True)
parser.add_argument("--month", help="month", required=True)
parser.add_argument("--day", help="day", required=True)
parser.add_argument("--meanTemp", help="meanTemp", required=True)
parser.add_argument("--meanRain", help="meanRain", required=True)
parser.add_argument("--meanSnow", help="meanSnow", required=True)
parser.add_argument("--ecoZone", help="ecoZone", required=True)
args = parser.parse_args()


with open('./ml/best_cause_model.pkl', 'rb') as file:
    model = pickle.load(file)


test_data = [
  {
    'LATITUDE': float(args.lat), 
    'LONGITUDE': float(args.lon),
    'YEAR': int(args.year),
    'MONTH': int(args.month),
    'DAY': int(args.day),
    'ECOZONE': int(args.ecoZone), # either 0, 6, 8, 15
    # 'PROVINCE_CODE': 'ON',
    'MEAN_TEMPERATURE': int(args.meanTemp),
    'MEAN_PRECIPITATION': int(args.meanRain),
    'MEAN_SNOWFALL': int(args.meanSnow),
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
# print(df_pred)

cause_name = df_pred[['CAUSE_H', 'CAUSE_H-PB', 'CAUSE_L', 'CAUSE_U']].max().idxmax()
fire_type_name = df_pred[['FIRE_TYPE_Fire', 'FIRE_TYPE_IFR', 'FIRE_TYPE_OFR', 'FIRE_TYPE_PB', 'FIRE_TYPE_Prescribed Burn']].max().idxmax()

# print('Fire size: ', df_pred['SIZE_HA'][0])
# print('Cause: ', cause_name)
# print('Fire type: ', fire_type_name)

fire_size = df_pred['SIZE_HA'][0]
cause = causeMap(cause_name)
fire_type = fire_type_name

df['SIZE_HA'] = fire_size
df['CAUSE'] = cause
df['FIRE_TYPE'] = fire_type

conn = sqlite3.connect('ml/pred.db')
df.to_sql('pred', conn, if_exists='replace', index=False)
print('success')