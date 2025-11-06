
import yfinance as yf
import json
from datetime import datetime
import time

class PriceAlertSystem:
    def __init__(self, alerts_file='price_alerts.json'):
        self.alerts_file = alerts_file
        self.alerts = self.load_alerts()

    def load_alerts(self):
        """Load alerts from JSON file"""
        try:
            with open(self.alerts_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'alerts': []}

    def save_alerts(self):
        """Save alerts to JSON file"""
        with open(self.alerts_file, 'w') as f:
            json.dump(self.alerts, f, indent=4)

    def add_alert(self, ticker, target_price, alert_type='above'):
        """
        Add price alert
        alert_type: 'above' or 'below'
        """
        alert = {
            'ticker': ticker,
            'target_price': target_price,
            'alert_type': alert_type,
            'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'triggered': False
        }

        self.alerts['alerts'].append(alert)
        self.save_alerts()
        print(f"Alert added: {ticker} {alert_type} ${target_price}")

    def remove_alert(self, ticker, target_price):
        """Remove a specific alert"""
        self.alerts['alerts'] = [
            a for a in self.alerts['alerts'] 
            if not (a['ticker'] == ticker and a['target_price'] == target_price)
        ]
        self.save_alerts()
        print(f"Alert removed: {ticker} at ${target_price}")

    def check_alerts(self):
        """Check all alerts and trigger notifications"""
        triggered_alerts = []

        for alert in self.alerts['alerts']:
            if alert['triggered']:
                continue

            ticker = alert['ticker']
            target_price = alert['target_price']
            alert_type = alert['alert_type']

            try:
                stock = yf.Ticker(ticker)
                current_price = stock.history(period='1d')['Close'].iloc[-1]

                triggered = False
                if alert_type == 'above' and current_price >= target_price:
                    triggered = True
                elif alert_type == 'below' and current_price <= target_price:
                    triggered = True

                if triggered:
                    alert['triggered'] = True
                    alert['triggered_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    alert['triggered_price'] = float(current_price)

                    triggered_alerts.append({
                        'ticker': ticker,
                        'target_price': target_price,
                        'current_price': current_price,
                        'alert_type': alert_type
                    })

                    print(f"\n🔔 ALERT TRIGGERED!")
                    print(f"   {ticker}: ${current_price:.2f} is {alert_type} target ${target_price:.2f}")

            except Exception as e:
                print(f"Error checking {ticker}: {e}")

        if triggered_alerts:
            self.save_alerts()

        return triggered_alerts

    def display_alerts(self):
        """Display all active alerts"""
        print("\n" + "="*60)
        print("ACTIVE PRICE ALERTS")
        print("="*60)

        active_alerts = [a for a in self.alerts['alerts'] if not a['triggered']]

        if not active_alerts:
            print("No active alerts")
        else:
            for alert in active_alerts:
                print(f"{alert['ticker']}: {alert['alert_type']} ${alert['target_price']:.2f}")

        print("="*60 + "\n")

    def monitor(self, check_interval=60):
        """
        Continuously monitor alerts
        check_interval: seconds between checks
        """
        print(f"Starting price alert monitor (checking every {check_interval} seconds)")
        print("Press Ctrl+C to stop\n")

        try:
            while True:
                self.check_alerts()
                time.sleep(check_interval)
        except KeyboardInterrupt:
            print("\nMonitoring stopped")

if __name__ == '__main__':
    # Example usage
    alert_system = PriceAlertSystem()

    # Add example alerts (uncomment to use)
    # alert_system.add_alert('TSLA', 300.00, 'above')
    # alert_system.add_alert('AAPL', 150.00, 'below')

    # Display alerts
    alert_system.display_alerts()

    # Check alerts once
    alert_system.check_alerts()

    # To monitor continuously (uncomment to use):
    # alert_system.monitor(check_interval=300)  # Check every 5 minutes
