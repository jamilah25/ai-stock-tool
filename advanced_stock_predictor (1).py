
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class AdvancedStockPredictor:
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = None
        self.models = {}

    def fetch_data(self):
        """Fetch stock data with additional technical indicators"""
        self.data = yf.download(self.ticker, start=self.start_date, end=self.end_date)

        # Add technical indicators
        self.data['MA_7'] = self.data['Close'].rolling(window=7).mean()
        self.data['MA_21'] = self.data['Close'].rolling(window=21).mean()
        self.data['RSI'] = self.calculate_rsi(self.data['Close'], 14)
        self.data['Volume_Change'] = self.data['Volume'].pct_change()

        self.data = self.data.dropna()
        return self.data

    def calculate_rsi(self, prices, period=14):
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def prepare_features(self):
        """Prepare features for ML models"""
        features = ['MA_7', 'MA_21', 'RSI', 'Volume_Change']
        X = self.data[features].values
        y = self.data['Close'].values

        # Create future prediction feature
        self.data['Day'] = np.arange(len(self.data))

        return X, y

    def train_models(self):
        """Train multiple ML models"""
        X, y = self.prepare_features()

        # Linear Regression
        lr_model = LinearRegression()
        lr_model.fit(X, y)
        self.models['Linear Regression'] = lr_model

        # Random Forest
        rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_model.fit(X, y)
        self.models['Random Forest'] = rf_model

        return self.models

    def predict(self, model_name='Random Forest'):
        """Make predictions using specified model"""
        X, y = self.prepare_features()
        model = self.models[model_name]
        predictions = model.predict(X)
        self.data['Predicted'] = predictions
        return predictions

    def plot_predictions(self, model_name='Random Forest'):
        """Plot actual vs predicted prices"""
        plt.figure(figsize=(12, 6))
        plt.plot(self.data.index, self.data['Close'], label='Actual Price', linewidth=2)
        plt.plot(self.data.index, self.data['Predicted'], label=f'{model_name} Prediction', linewidth=2, linestyle='--')
        plt.title(f'{self.ticker} Stock Price Prediction using {model_name}')
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig(f'{self.ticker}_{model_name.replace(" ", "_")}_prediction.png')
        plt.close()

    def calculate_accuracy(self):
        """Calculate prediction accuracy metrics"""
        actual = self.data['Close'].values
        predicted = self.data['Predicted'].values

        mse = np.mean((actual - predicted) ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(actual - predicted))

        return {'MSE': mse, 'RMSE': rmse, 'MAE': mae}

if __name__ == '__main__':
    # Example usage
    predictor = AdvancedStockPredictor('TSLA', '2023-01-01', '2025-11-01')
    predictor.fetch_data()
    predictor.train_models()

    # Test both models
    for model_name in ['Linear Regression', 'Random Forest']:
        predictor.predict(model_name)
        predictor.plot_predictions(model_name)
        accuracy = predictor.calculate_accuracy()
        print(f"{model_name} Accuracy Metrics:")
        print(f"  RMSE: ${accuracy['RMSE']:.2f}")
        print(f"  MAE: ${accuracy['MAE']:.2f}")
        print()
