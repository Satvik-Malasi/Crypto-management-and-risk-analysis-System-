# main.py

from RestApi.mainREST import RestAPIClient
from portfolioUtility.latestPrice import latestPrice
from portfolioUtility.portfolioCalculator import PortfolioCalculator
from portfolioUtility.reportGeneration import ReportGenerator
import os

def main():
    # === CONFIGURATION ===
    REST_API_KEY = "E7LHCW66U9WKNNSD"   # Alpha Vantage key
    WS_API_KEY = "d3gki79r01qpep678tn0d3gki79r01qpep678tng"  # Finnhub key
    INTERVAL = "30min"
    DATA_DIR = "data"
    os.makedirs(DATA_DIR, exist_ok=True)

    # === USER PORTFOLIO ===
    holdings = {
    "BTC": 0.05,   # 0.05 BTC
    "ETH": 0.8,    # 0.8 ETH
    "DOT": 50,     # Polkadot
    "BNB": 2,      # Binance Coin
    "XRP": 500,    # Ripple
    "LTC": 5 
    }

    # === STEP 1: FETCH HISTORICAL DATA (REST API) ===
    rest_client = RestAPIClient(REST_API_KEY)
    historical_data_paths = {}
    for symbol in holdings.keys():
        print(f"\n📡 Fetching historical data for {symbol}...")
        candles = rest_client.fetch_intraday_candles(symbol, INTERVAL)
        file_path = os.path.join(DATA_DIR, f"{symbol}_{INTERVAL}.csv")
        rest_client.save_to_csv(candles, file_path)
        historical_data_paths[symbol] = file_path

    # === STEP 2: FETCH LIVE PRICES (WebSocket) ===
    live_prices = {}
    for symbol in holdings.keys():
        print(f"\n💹 Fetching live price for {symbol}...")
        fetcher = latestPrice(WS_API_KEY, [f"BINANCE:{symbol}USDT"], f"{DATA_DIR}/{symbol}_live.csv")
        tick = fetcher.get_latest_tick()
        if tick:
            live_prices[symbol] = tick["price"]
        else:
            print(f"⚠️ Could not fetch live price for {symbol}, skipping.")
            live_prices[symbol] = 0

    # === STEP 3: CALCULATE PORTFOLIO METRICS ===
    print("\n📈 Calculating portfolio metrics...")
    calc = PortfolioCalculator(holdings, historical_data_paths, live_prices)
    metrics = (
        calc.load_data()
            .compute_returns()
            .compute_portfolio_metrics()
    )

    # === STEP 4: GENERATE REPORT ===
    print("\n🧾 Generating PDF report...")
    report = ReportGenerator("portfolio_report.pdf")
    report.generate(metrics, holdings)

    print("\n✅ Process completed successfully!")

if __name__ == "__main__":
    main()
