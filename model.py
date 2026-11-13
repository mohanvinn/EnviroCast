import pandas as pd
import os
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from statsmodels.tsa.arima.model import ARIMA

def train_model():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(current_dir, "data.csv"))

    X = df[["PM2.5", "PM10", "NO2", "CO", "SO2", "O3"]]
    y = df["AQI"]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # --- Model 1: Linear Regression ---
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    lr_pred = lr_model.predict(X_test)

    # --- Model 2: Random Forest ---
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)

    # --- Accuracy Metrics ---
    lr_r2 = r2_score(y_test, lr_pred)
    rf_r2 = r2_score(y_test, rf_pred)

    lr_mae = mean_absolute_error(y_test, lr_pred)
    rf_mae = mean_absolute_error(y_test, rf_pred)

    # --- Choose Best Model ---
    best_model = rf_model if rf_r2 > lr_r2 else lr_model
    best_name = "Random Forest" if rf_r2 > lr_r2 else "Linear Regression"

    metrics = {
        "Linear Regression R2": lr_r2,
        "Random Forest R2": rf_r2,
        "Linear Regression MAE": lr_mae,
        "Random Forest MAE": rf_mae,
        "Best Model": best_name
    }

    return best_model, df, metrics


def predict_aqi(model, pm25, pm10, no2, co, so2, o3):
    # కాలమ్ నేమ్స్‌తో సహా డేటాను పంపడం
    input_data = pd.DataFrame([[pm25, pm10, no2, co, so2, o3]], 
                              columns=["PM2.5", "PM10", "NO2", "CO", "SO2", "O3"])
    prediction = model.predict(input_data)
    return prediction[0]


def forecast_future_aqi(data_series, steps=7):
    # 'data_series' అనేది మీ గత 24-30 రోజుల AQI డేటా అయి ఉండాలి
    model = ARIMA(data_series, order=(5,1,0)) # (p,d,q) parameters
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=steps)
    return forecast  ,model.py