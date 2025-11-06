
import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import tempfile

st.title("Simple Stock Price Prediction Tool")

ticker = st.text_input("Enter stock ticker (e.g., TSLA):", "TSLA")
start_date = st.date_input("Start date:", pd.to_datetime("2023-01-01"))
end_date = st.date_input("End date:", pd.to_datetime("2025-11-01"))

if st.button("Fetch and Predict"):
    data = yf.download(ticker, start=start_date, end=end_date)
    if data.empty:
        st.write("No data found. Please check the ticker and dates.")
    else:
        data = data[['Close']].dropna()
        data['Day'] = np.arange(len(data.index))
        X = data['Day'].values.reshape(-1, 1)
        y = data['Close'].values

        model = LinearRegression()
        model.fit(X, y)

        data['Predicted'] = model.predict(X)

        st.line_chart(data[['Close', 'Predicted']])

        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
            plt.figure(figsize=(10, 5))
            plt.plot(data.index, data['Close'], label='Actual')
            plt.plot(data.index, data['Predicted'], label='Predicted')
            plt.title(f'{ticker} Stock Price Prediction')
            plt.xlabel('Date')
            plt.ylabel('Price USD')
            plt.legend()
            plt.savefig(tmpfile.name)
            plt.close()
            st.image(tmpfile.name, caption='Stock Price Prediction Chart')
