from flask import Flask, render_template, request
import yfinance as yf
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    stock_data = None
    error = None

    if request.method == 'POST':
        symbol = request.form.get('symbol')
        try:
            stock = yf.Ticker(symbol)
            stock_info = stock.info

            company_name = stock_info.get('longName')
            current_price = stock_info.get('currentPrice')
            previous_close = stock_info.get('previousClose')

            if company_name is None or current_price is None or previous_close is None:
                raise ValueError("Invalid stock symbol or incomplete data.")

            value_change = current_price - previous_close
            percentage_change = (value_change / previous_close) * 100

            timezone = pytz.timezone("America/Los_Angeles")
            now = datetime.now(timezone)
            current_time = now.strftime("%a %b %d %H:%M:%S %Z %Y")

            sign = "+" if value_change >= 0 else ""

            stock_data = {
                'time': current_time,
                'company_name': company_name,
                'symbol': symbol.upper(),
                'price': f"{current_price:.2f}",
                'value_change': f"{sign}{value_change:.2f}",
                'percentage_change': f"{sign}{percentage_change:.2f}%"
            }

        except Exception as e:
            error = f"Error: {str(e)}"

    return render_template('index.html', stock_data=stock_data, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

