
import yfinance as yf
import pandas as pd
import json
from datetime import datetime

class PortfolioTracker:
    def __init__(self, portfolio_file='portfolio.json'):
        self.portfolio_file = portfolio_file
        self.portfolio = self.load_portfolio()

    def load_portfolio(self):
        """Load portfolio from JSON file"""
        try:
            with open(self.portfolio_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'stocks': []}

    def save_portfolio(self):
        """Save portfolio to JSON file"""
        with open(self.portfolio_file, 'w') as f:
            json.dump(self.portfolio, f, indent=4)

    def add_stock(self, ticker, shares, purchase_price, purchase_date=None):
        """Add a stock to portfolio"""
        if purchase_date is None:
            purchase_date = datetime.now().strftime('%Y-%m-%d')

        stock_entry = {
            'ticker': ticker,
            'shares': shares,
            'purchase_price': purchase_price,
            'purchase_date': purchase_date
        }

        self.portfolio['stocks'].append(stock_entry)
        self.save_portfolio()
        print(f"Added {shares} shares of {ticker} at ${purchase_price}")

    def remove_stock(self, ticker):
        """Remove a stock from portfolio"""
        self.portfolio['stocks'] = [s for s in self.portfolio['stocks'] if s['ticker'] != ticker]
        self.save_portfolio()
        print(f"Removed {ticker} from portfolio")

    def get_current_prices(self):
        """Fetch current prices for all stocks in portfolio"""
        tickers = [stock['ticker'] for stock in self.portfolio['stocks']]
        if not tickers:
            return {}

        prices = {}
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                current_price = stock.history(period='1d')['Close'].iloc[-1]
                prices[ticker] = current_price
            except:
                prices[ticker] = None

        return prices

    def calculate_portfolio_value(self):
        """Calculate total portfolio value and performance"""
        current_prices = self.get_current_prices()

        total_investment = 0
        total_current_value = 0

        results = []

        for stock in self.portfolio['stocks']:
            ticker = stock['ticker']
            shares = stock['shares']
            purchase_price = stock['purchase_price']
            current_price = current_prices.get(ticker)

            if current_price is None:
                continue

            investment = shares * purchase_price
            current_value = shares * current_price
            profit_loss = current_value - investment
            profit_loss_pct = (profit_loss / investment) * 100

            total_investment += investment
            total_current_value += current_value

            results.append({
                'Ticker': ticker,
                'Shares': shares,
                'Purchase Price': f'${purchase_price:.2f}',
                'Current Price': f'${current_price:.2f}',
                'Investment': f'${investment:.2f}',
                'Current Value': f'${current_value:.2f}',
                'Profit/Loss': f'${profit_loss:.2f}',
                'Profit/Loss %': f'{profit_loss_pct:.2f}%'
            })

        total_profit_loss = total_current_value - total_investment
        total_profit_loss_pct = (total_profit_loss / total_investment * 100) if total_investment > 0 else 0

        return {
            'stocks': results,
            'total_investment': total_investment,
            'total_current_value': total_current_value,
            'total_profit_loss': total_profit_loss,
            'total_profit_loss_pct': total_profit_loss_pct
        }

    def display_portfolio(self):
        """Display portfolio summary"""
        summary = self.calculate_portfolio_value()

        print("\n" + "="*80)
        print("PORTFOLIO SUMMARY")
        print("="*80)

        df = pd.DataFrame(summary['stocks'])
        if not df.empty:
            print(df.to_string(index=False))
        else:
            print("No stocks in portfolio")

        print("\n" + "-"*80)
        print(f"Total Investment:    ${summary['total_investment']:.2f}")
        print(f"Current Value:       ${summary['total_current_value']:.2f}")
        print(f"Profit/Loss:         ${summary['total_profit_loss']:.2f}")
        print(f"Return:              {summary['total_profit_loss_pct']:.2f}%")
        print("="*80 + "\n")

if __name__ == '__main__':
    # Example usage
    tracker = PortfolioTracker()

    # Add some example stocks (uncomment to use)
    # tracker.add_stock('TSLA', 10, 250.00, '2024-01-01')
    # tracker.add_stock('AAPL', 5, 180.00, '2024-01-01')
    # tracker.add_stock('GOOGL', 3, 140.00, '2024-01-01')

    # Display portfolio
    tracker.display_portfolio()
