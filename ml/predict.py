import joblib
import pandas as pd
import argparse
import re

def pred(lat, lon, year, month, day, province, cause):
    '''
    load the model and predict the results
    '''
    # Load the trained model from the .pkl file
    loaded_model = joblib.load('./models/optimized_xgb_regression_model.pkl')

    # Prepare a new DataFrame with input features for prediction
    # Make sure the column order matches the order of 'predictors'
    input_data = pd.DataFrame({
        'LATITUDE': [lat],
        'LONGITUDE': [lon],
        'YEAR': [int(year)],
        'MONTH': [int(month)],
        'DAY': [int(day)],
        'SRC_AGENCY_AB': [match(province, 'SRC_AGENCY_AB')],                  # Replace with 0 or 1 based on the presence of the agency
        'SRC_AGENCY_BC': [match(province, 'SRC_AGENCY_BC')],                  # Replace with 0 or 1 based on the presence of the agency
        'SRC_AGENCY_MB': [match(province, 'SRC_AGENCY_MB')],                  # Replace with 0 or 1 based on the presence of the agency
        'SRC_AGENCY_NB': [match(province, 'SRC_AGENCY_NB')],                  # Replace with 0 or 1 based on the presence of the agency
        'SRC_AGENCY_NL': [match(province, 'SRC_AGENCY_NL')],                  # Replace with 0 or 1 based on the presence of the agency
        'SRC_AGENCY_NS': [match(province, 'SRC_AGENCY_NS')],                  # Replace with 0 or 1 based on the presence of the agency
        'SRC_AGENCY_NT': [match(province, 'SRC_AGENCY_NT')],                  # Replace with 0 or 1 based on the presence of the agency
        'SRC_AGENCY_ON': [match(province, 'SRC_AGENCY_ON')],                  # Replace with 0 or 1 based on the presence of the agency
        'SRC_AGENCY_QC': [match(province, 'SRC_AGENCY_OC')],                  # Replace with 0 or 1 based on the presence of the agency
        'SRC_AGENCY_SK': [match(province, 'SRC_AGENCY_SK')],                  # Replace with 0 or 1 based on the presence of the agency
        'SRC_AGENCY_YT': [match(province, 'SRC_AGENCY_YT')],                  # Replace with 0 or 1 based on the presence of the agency
        'CAUSE_H': [match(cause, 'CAUSE_H')],                        # Replace with 0 or 1 based on the presence of the cause
        'CAUSE_H-PB': [match(cause, 'CAUSE_H-PB')],                     # Replace with 0 or 1 based on the presence of the cause
        'CAUSE_L': [match(cause, 'CAUSE_L')],                        # Replace with 0 or 1 based on the presence of the cause
        'CAUSE_RE': [match(cause, 'CAUSE_RE')],                       # Replace with 0 or 1 based on the presence of the cause
        'CAUSE_U': [match(cause, 'CAUSE_U')]                         # Replace with 0 or 1 based on the presence of the cause
    })

    # Make predictions using the loaded model
    predictions = loaded_model.predict(input_data)
    print("Predicted SIZE_HA values:", predictions)

def match(a, b):
    pattern = re.escape(a) + r'$'
    if re.search(pattern, b):
        return 1
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", help="lat", type=float, default=43.651070)
    parser.add_argument("--lon", help="lon", type=float, default=-79.347015)
    parser.add_argument("--year", help="year", type=int, default=2023)
    parser.add_argument("--month", help="month", type=int, default=7)
    parser.add_argument("--day", help="day", type=int, default=1)
    parser.add_argument("--province", help="province", type=str, default="ON")
    parser.add_argument("--cause", help="cause", type=str, default="H")
    args = parser.parse_args()
    
    pred(args.lat, args.lon, args.year, args.month, args.day, args.province, args.cause)