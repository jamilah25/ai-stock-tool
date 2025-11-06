# AI-Driven Stock Prediction Tool

A simple yet powerful stock prediction tool that uses AI/Machine Learning to analyze and predict stock price trends.

## Overview

This tool provides three main components:
1. **Basic Stock Data Fetcher** - Fetches and visualizes historical stock prices
2. **AI Prediction Model** - Uses Linear Regression to predict stock price trends
3. **Web Application** - Interactive interface for easy stock analysis

## Requirements

- Python 3.7 or higher
- Internet connection (to fetch stock data)

## Installation Instructions

### Step 1: Install Python
If you don't have Python installed:
- Download from [python.org](https://www.python.org/downloads/)
- During installation, check "Add Python to PATH"

### Step 2: Install Required Libraries
Open Command Prompt (Windows) or Terminal (Mac/Linux) and run:

```bash
pip install yfinance numpy pandas scikit-learn matplotlib streamlit
```

### Step 3: Download the Tool Files
Download these three files to a folder on your computer:
- `stock_tool_prototype.py`
- `stock_price_prediction.py`
- `stock_prediction_app.py`

## How to Use

### Option 1: Run the Web App (Recommended for Beginners)
1. Open Command Prompt/Terminal
2. Navigate to the folder containing the files:
   ```bash
   cd path/to/your/folder
   ```
3. Run the web app:
   ```bash
   streamlit run stock_prediction_app.py
   ```
4. Your browser will open automatically with the app interface
5. Enter a stock ticker (e.g., TSLA, AAPL, GOOGL)
6. Select date range
7. Click "Fetch and Predict" to see results

### Option 2: Run Individual Scripts
**Basic Stock Fetcher:**
```bash
python stock_tool_prototype.py
```
This will save a chart image of Tesla's stock prices.

**AI Prediction Model:**
```bash
python stock_price_prediction.py
```
This will create a prediction chart comparing actual vs predicted prices.

## Understanding the Tool

### What Each File Does:

**stock_tool_prototype.py**
- Fetches historical stock data from Yahoo Finance
- Creates a visualization of closing prices
- Saves the chart as a PNG image

**stock_price_prediction.py**
- Downloads stock data
- Trains a Linear Regression AI model
- Predicts future price trends
- Compares actual vs predicted prices

**stock_prediction_app.py**
- Provides a user-friendly web interface
- Allows you to input any stock ticker
- Displays interactive charts
- Shows predictions in real-time

## Common Stock Tickers to Try

- **TSLA** - Tesla
- **AAPL** - Apple
- **GOOGL** - Google
- **MSFT** - Microsoft
- **AMZN** - Amazon
- **NVDA** - Nvidia
- **META** - Meta (Facebook)

## Monetization Ideas

### 1. Offer as a Subscription Service
- Basic tier: Free with limited stocks
- Premium tier: $10-20/month with advanced features

### 2. Freelance Services
- Offer stock analysis reports to clients
- Charge per analysis or monthly retainer

### 3. Content Creation
- Create YouTube videos showing how to use it
- Write blog posts with stock insights
- Monetize through ads and affiliate links

### 4. Expand Features (Premium Version)
- Add multiple AI models (LSTM, Random Forest)
- Real-time alerts via email/SMS
- Portfolio tracking
- Risk analysis tools

## Troubleshooting

**"Command not found" error:**
- Make sure Python is installed and added to PATH
- Try `python3` instead of `python`

**"No module named" error:**
- Run the pip install command again
- Make sure you're in the correct Python environment

**"No data found" error:**
- Check your internet connection
- Verify the stock ticker is correct
- Try a different date range

**Web app won't open:**
- Check if port 8501 is available
- Try: `streamlit run stock_prediction_app.py --server.port 8502`

## Next Steps to Improve

1. Add more sophisticated AI models (LSTM, GRU for time series)
2. Include technical indicators (RSI, MACD, Moving Averages)
3. Add portfolio management features
4. Implement email/SMS alerts for price changes
5. Create mobile app version
6. Add cryptocurrency support
7. Include news sentiment analysis

## Support

For questions or issues:
- Check Python and library documentation
- Search Stack Overflow for specific errors
- Review Yahoo Finance API documentation

## Legal Disclaimer

This tool is for educational and informational purposes only. Stock predictions are not guaranteed to be accurate. Always do your own research before making investment decisions. Past performance does not guarantee future results.

## License

This project is provided as-is for personal and educational use.

---

**Created:** November 2025
**Version:** 1.0
**Author:** AI-Driven Investment Tool
