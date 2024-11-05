import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

def predict_temperature():
    # Load model and scaler
    model = load_model("tem_predict_next_2_hours.keras")
    scaler_temp = MinMaxScaler(feature_range=(0, 1))

    # Load data and preprocess
    data = pd.read_csv('history.csv')
    data['TimeStamp'] = pd.to_datetime(data['TimeStamp'])
    data.set_index('TimeStamp', inplace=True)
    data['Temperature'] = scaler_temp.fit_transform(data[['Temperature']])

    # Prepare latest sequence (last 24 hours) for prediction
    latest_sequence = data[['Temperature']].values[-24:]
    latest_sequence = latest_sequence.reshape(1, 24, 1)  # Reshape for model input

    # Predict next 2 hours and inverse transform
    predicted_temp_scaled = model.predict(latest_sequence)
    predicted_temp = scaler_temp.inverse_transform(predicted_temp_scaled)

    return predicted_temp[0][0], predicted_temp[0][1]

predict_temperature()