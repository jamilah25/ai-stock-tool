
import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(page_title="AI Stock & Crypto Analysis Tool", layout="wide")

# Initialize session state
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []
if 'alerts' not in st.session_state:
    st.session_state.alerts = []

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Stock Prediction", "Portfolio Tracker", "Price Alerts", "Crypto Tracker", "Market Overview"])

# Helper functions
def calculate_rsi(prices, period=14):
    """Calculate RSI indicator"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def predict_stock(ticker, start_date, end_date, model_type='Random Forest'):
    """Predict stock prices using ML"""
    try:
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)

        if data.empty:
            return None, "No data found"

        # Technical indicators
        data['MA_7'] = data['Close'].rolling(window=7).mean()
        data['MA_21'] = data['Close'].rolling(window=21).mean()
        data['RSI'] = calculate_rsi(data['Close'])
        data['Volume_Change'] = data['Volume'].pct_change()
        data = data.dropna()

        # Prepare features
        features = ['MA_7', 'MA_21', 'RSI', 'Volume_Change']
        X = data[features].values
        y = data['Close'].values

        # Train model
        if model_type == 'Linear Regression':
            model = LinearRegression()
        else:
            model = RandomForestRegressor(n_estimators=100, random_state=42)

        model.fit(X, y)
        data['Predicted'] = model.predict(X)

        return data, None

    except Exception as e:
        return None, str(e)

# Page 1: Stock Prediction
if page == "Stock Prediction":
    st.title("📈 AI Stock Price Prediction")

    col1, col2, col3 = st.columns(3)

    with col1:
        ticker = st.text_input("Stock Ticker", "TSLA")
    with col2:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=365))
    with col3:
        end_date = st.date_input("End Date", datetime.now())

    model_type = st.selectbox("Select AI Model", ["Random Forest", "Linear Regression"])

    if st.button("Analyze Stock"):
        with st.spinner("Fetching data and training model..."):
            data, error = predict_stock(ticker, start_date, end_date, model_type)

            if error:
                st.error(f"Error: {error}")
            else:
                st.success(f"Analysis complete for {ticker}")

                # Plot
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Actual Price', line=dict(color='blue', width=2)))
                fig.add_trace(go.Scatter(x=data.index, y=data['Predicted'], name='Predicted Price', line=dict(color='red', width=2, dash='dash')))
                fig.update_layout(title=f'{ticker} Price Prediction', xaxis_title='Date', yaxis_title='Price (USD)', height=500)
                st.plotly_chart(fig, use_container_width=True)

                # Metrics
                col1, col2, col3, col4 = st.columns(4)
                current_price = data['Close'].iloc[-1]
                predicted_price = data['Predicted'].iloc[-1]
                change = ((predicted_price - current_price) / current_price) * 100

                col1.metric("Current Price", f"${current_price:.2f}")
                col2.metric("Predicted Price", f"${predicted_price:.2f}")
                col3.metric("Prediction Change", f"{change:.2f}%")
                col4.metric("RSI", f"{data['RSI'].iloc[-1]:.2f}")

# Page 2: Portfolio Tracker
elif page == "Portfolio Tracker":
    st.title("💼 Portfolio Tracker")

    # Add stock to portfolio
    st.subheader("Add Stock to Portfolio")
    col1, col2, col3 = st.columns(3)

    with col1:
        new_ticker = st.text_input("Ticker Symbol")
    with col2:
        new_shares = st.number_input("Number of Shares", min_value=0.01, step=0.01)
    with col3:
        new_price = st.number_input("Purchase Price", min_value=0.01, step=0.01)

    if st.button("Add to Portfolio"):
        if new_ticker:
            st.session_state.portfolio.append({
                'ticker': new_ticker.upper(),
                'shares': new_shares,
                'purchase_price': new_price,
                'date': datetime.now().strftime('%Y-%m-%d')
            })
            st.success(f"Added {new_shares} shares of {new_ticker} to portfolio")

    # Display portfolio
    if st.session_state.portfolio:
        st.subheader("Your Portfolio")

        portfolio_data = []
        total_investment = 0
        total_value = 0

        for stock in st.session_state.portfolio:
            try:
                ticker_obj = yf.Ticker(stock['ticker'])
                current_price = ticker_obj.history(period='1d')['Close'].iloc[-1]

                investment = stock['shares'] * stock['purchase_price']
                current_value = stock['shares'] * current_price
                profit_loss = current_value - investment
                profit_loss_pct = (profit_loss / investment) * 100

                total_investment += investment
                total_value += current_value

                portfolio_data.append({
                    'Ticker': stock['ticker'],
                    'Shares': stock['shares'],
                    'Purchase Price': f"${stock['purchase_price']:.2f}",
                    'Current Price': f"${current_price:.2f}",
                    'Investment': f"${investment:.2f}",
                    'Current Value': f"${current_value:.2f}",
                    'Profit/Loss': f"${profit_loss:.2f}",
                    'Return %': f"{profit_loss_pct:.2f}%"
                })
            except:
                continue

        if portfolio_data:
            df = pd.DataFrame(portfolio_data)
            st.dataframe(df, use_container_width=True)

            # Summary metrics
            total_profit = total_value - total_investment
            total_return = (total_profit / total_investment * 100) if total_investment > 0 else 0

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Investment", f"${total_investment:.2f}")
            col2.metric("Current Value", f"${total_value:.2f}")
            col3.metric("Total Profit/Loss", f"${total_profit:.2f}")
            col4.metric("Total Return", f"{total_return:.2f}%")
    else:
        st.info("No stocks in portfolio. Add your first stock above!")

# Page 3: Price Alerts
elif page == "Price Alerts":
    st.title("🔔 Price Alerts")

    # Add alert
    st.subheader("Create Price Alert")
    col1, col2, col3 = st.columns(3)

    with col1:
        alert_ticker = st.text_input("Ticker Symbol")
    with col2:
        alert_price = st.number_input("Target Price", min_value=0.01, step=0.01)
    with col3:
        alert_type = st.selectbox("Alert When Price Is", ["Above", "Below"])

    if st.button("Create Alert"):
        if alert_ticker:
            st.session_state.alerts.append({
                'ticker': alert_ticker.upper(),
                'target_price': alert_price,
                'alert_type': alert_type.lower(),
                'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            st.success(f"Alert created for {alert_ticker} {alert_type.lower()} ${alert_price}")

    # Display alerts
    if st.session_state.alerts:
        st.subheader("Active Alerts")

        alert_data = []
        for alert in st.session_state.alerts:
            try:
                ticker_obj = yf.Ticker(alert['ticker'])
                current_price = ticker_obj.history(period='1d')['Close'].iloc[-1]

                status = "🔴 Not Triggered"
                if alert['alert_type'] == 'above' and current_price >= alert['target_price']:
                    status = "🟢 TRIGGERED!"
                elif alert['alert_type'] == 'below' and current_price <= alert['target_price']:
                    status = "🟢 TRIGGERED!"

                alert_data.append({
                    'Ticker': alert['ticker'],
                    'Target Price': f"${alert['target_price']:.2f}",
                    'Current Price': f"${current_price:.2f}",
                    'Condition': alert['alert_type'].title(),
                    'Status': status
                })
            except:
                continue

        if alert_data:
            df = pd.DataFrame(alert_data)
            st.dataframe(df, use_container_width=True)
    else:
        st.info("No active alerts. Create your first alert above!")

# Page 4: Crypto Tracker
elif page == "Crypto Tracker":
    st.title("₿ Cryptocurrency Tracker")

    crypto_symbols = ['BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'DOGE', 'SOL', 'DOT', 'MATIC', 'LTC']

    st.subheader("Top Cryptocurrencies")

    crypto_data = []
    for symbol in crypto_symbols:
        try:
            ticker = f"{symbol}-USD"
            crypto = yf.Ticker(ticker)
            history = crypto.history(period='1d')

            if not history.empty:
                current_price = history['Close'].iloc[-1]
                day_high = history['High'].iloc[-1]
                day_low = history['Low'].iloc[-1]

                crypto_data.append({
                    'Symbol': symbol,
                    'Price': f"${current_price:.2f}",
                    '24h High': f"${day_high:.2f}",
                    '24h Low': f"${day_low:.2f}"
                })
        except:
            continue

    if crypto_data:
        df = pd.DataFrame(crypto_data)
        st.dataframe(df, use_container_width=True)

    # Individual crypto analysis
    st.subheader("Analyze Cryptocurrency")
    selected_crypto = st.selectbox("Select Cryptocurrency", crypto_symbols)

    if st.button("Analyze"):
        ticker = f"{selected_crypto}-USD"
        data = yf.download(ticker, period='1mo', progress=False)

        if not data.empty:
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']))
            fig.update_layout(title=f'{selected_crypto} Price Chart (30 Days)', xaxis_title='Date', yaxis_title='Price (USD)', height=500)
            st.plotly_chart(fig, use_container_width=True)

# Page 5: Market Overview
elif page == "Market Overview":
    st.title("🌍 Market Overview")

    # Major indices
    st.subheader("Major Market Indices")

    indices = {
        'S&P 500': '^GSPC',
        'Dow Jones': '^DJI',
        'NASDAQ': '^IXIC',
        'Russell 2000': '^RUT'
    }

    index_data = []
    for name, ticker in indices.items():
        try:
            index = yf.Ticker(ticker)
            history = index.history(period='2d')

            if len(history) >= 2:
                current = history['Close'].iloc[-1]
                previous = history['Close'].iloc[-2]
                change = current - previous
                change_pct = (change / previous) * 100

                index_data.append({
                    'Index': name,
                    'Value': f"{current:.2f}",
                    'Change': f"{change:+.2f}",
                    'Change %': f"{change_pct:+.2f}%"
                })
        except:
            continue

    if index_data:
        df = pd.DataFrame(index_data)
        st.dataframe(df, use_container_width=True)

    # Trending stocks
    st.subheader("Popular Stocks")
    popular_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX']

    stock_data = []
    for ticker in popular_stocks:
        try:
            stock = yf.Ticker(ticker)
            history = stock.history(period='1d')

            if not history.empty:
                price = history['Close'].iloc[-1]
                stock_data.append({
                    'Ticker': ticker,
                    'Price': f"${price:.2f}"
                })
        except:
            continue

    if stock_data:
        df = pd.DataFrame(stock_data)
        st.dataframe(df, use_container_width=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.info("AI Stock & Crypto Analysis Tool v2.0")
