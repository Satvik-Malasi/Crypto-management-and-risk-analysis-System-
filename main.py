# # # main.py

# from services.email_sender import EmailSender
# from RestApi.mainREST import RestAPIClient
# from portfolioUtility.latestprice_throughRest import latestprice_throughRest
# from portfolioUtility.portfolioCalculator import PortfolioCalculator
# from portfolioUtility.reportGeneration import ReportGenerator
# import os

# def main():
#     # === CONFIGURATION ===
#     REST_API_KEY = "E7LHCW66U9WKNNSD"   # Alpha Vantage key
#     WS_API_KEY = "d3gki79r01qpep678tn0d3gki79r01qpep678tng"  # Finnhub key
#     INTERVAL = "30min"
#     DATA_DIR = "data"
#     os.makedirs(DATA_DIR, exist_ok=True)

#     # === USER PORTFOLIO ===
#     holdings = {
#     # "BTC": 6,   # 0.05 BTC
#     # "ETH": 3,    # 0.8 ETH
#     # "LTC": 100

#     "AAPL":20, 
#     "MSFT":20,
#     "GOOGL":30,
#     "AMZN":45,
#     "TSLA":55
#     # "FB":31,
#     # "NVDA":11,
#     # "NFLX": 54,
#     # "JPM":87,
#     # "BAC":22
#     }

#     # === STEP 1: FETCH HISTORICAL DATA (REST API) ===
#     rest_client = RestAPIClient(REST_API_KEY)
#     historical_data_paths = {}
#     for symbol in holdings.keys():
#         print(f"\n📡 Fetching historical data for {symbol}...")
#         candles = rest_client.fetch_intraday_candles(symbol, INTERVAL)
#         file_path = os.path.join(DATA_DIR, f"{symbol}_{INTERVAL}.csv")
#         rest_client.save_to_csv(candles, file_path)
#         historical_data_paths[symbol] = file_path

#     # === STEP 2: FETCH LIVE PRICES (WebSocket) ===
#     live_prices = {}
#     for symbol in holdings.keys():
#         print(f"\n💹 Fetching live price for {symbol}...")
#         fetcher = latestprice_throughRest(WS_API_KEY, [f"BINANCE:{symbol}USDT"], f"{DATA_DIR}/{symbol}_live.csv")
#         tick = fetcher.get_latest_tick()
#         if tick:
#             live_prices[symbol] = tick["price"]
#         else:
#             print(f"⚠️ Could not fetch live price for {symbol}, skipping.")
#             live_prices[symbol] = 0

#     # === STEP 3: CALCULATE PORTFOLIO METRICS ===
#     print("\n📈 Calculating portfolio metrics...")
#     calc = PortfolioCalculator(holdings, historical_data_paths, live_prices)
#     metrics = (
#         calc.load_data()
#             .compute_returns()
#             .compute_portfolio_metrics()
#     )

#     # === STEP 4: GENERATE REPORT ===
#     print("\n🧾 Generating PDF report...")
#     report = ReportGenerator("portfolio_report.pdf")
#     report.generate(metrics, holdings)

#     # --- Send report via email ---

#     SENDER_EMAIL = "shivamBhai12102025@gmail.com"
#     SENDER_PASSWORD = "crvm lkjh tgxd qtkx"  # use an app password if Gmail
#     RECEIVER_EMAIL = "rajrawat2557@gmail.com"
    
#     emailer = EmailSender(SENDER_EMAIL, SENDER_PASSWORD)
#     emailer.send_email(
#         to_email=RECEIVER_EMAIL,
#         subject="📊 Portfolio Report",
#         body="Hi,\n\nPlease find attached the latest crypto portfolio report.\n\n- Automated System",
#         attachment_path=r"D:\javaProjectsVsCode\python programs\finnhubApi\portfolio_report.pdf"
#     )


#     print("\n✅ Process completed successfully!")

# if __name__ == "__main__":
#     main()


# main.py


import os
from services.email_sender import EmailSender
from RestApi.mainREST import RestAPIClient
from portfolioUtility.latestprice_throughRest import latestprice_throughRest
from portfolioUtility.portfolioCalculator import PortfolioCalculator
from portfolioUtility.reportGeneration import ReportGenerator
from portfolioUtility.hybrid_price_fetcher import fetch_latest_prices

def main():
    # === CONFIGURATION ===
    REST_API_KEY = "E7LHCW66U9WKNNSD"   # Alpha Vantage key
    WS_API_KEY = "d3gki79r01qpep678tn0d3gki79r01qpep678tng"  # Finnhub key
    INTERVAL = "30min"
    DATA_DIR = "data"
    os.makedirs(DATA_DIR, exist_ok=True)

    # === USER PORTFOLIO ===
    holdings = {
        "AAPL": 20,
        "MSFT": 20,
        "GOOGL": 30,
        "AMZN": 45,
        "TSLA": 55,
        "FB": 31,
        "NVDA": 11,
        "NFLX": 54,
        "JPM": 87,
        "BAC": 22
    }

    # === STEP 1: FETCH HISTORICAL DATA (REST API) ===
    # rest_client = RestAPIClient(REST_API_KEY)
    # historical_data_paths = {}

    # for symbol in holdings.keys():
    #     print(f"\n📡 Fetching historical data for {symbol}...")
    #     candles = rest_client.fetch_intraday_candles(symbol, INTERVAL)
    #     file_path = os.path.join(DATA_DIR, f"{symbol}_{INTERVAL}.csv")
    #     rest_client.save_to_csv(candles, file_path)
    #     historical_data_paths[symbol] = file_path

     # === STEP 1: USE EXISTING HISTORICAL CSV FILES ===
    print("\n📂 Using existing historical CSV files...")
    historical_data_paths = {}
    for symbol in holdings.keys():
        file_path = os.path.join(DATA_DIR, f"{symbol}_{INTERVAL}.csv")
        if os.path.exists(file_path):
            historical_data_paths[symbol] = file_path
            print(f"✅ Found {symbol} data at {file_path}")
        else:
            print(f"⚠️ Missing CSV for {symbol}: {file_path}")


    # === STEP 2: FETCH LIVE PRICES (Hybrid: WebSocket → CSV → REST) ===
    print("\n💹 Fetching latest prices (Hybrid)...")
    live_prices = fetch_latest_prices(holdings.keys(), WS_API_KEY,REST_API_KEY,  DATA_DIR, interval=INTERVAL)

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

    # === STEP 5: EMAIL REPORT ===
    SENDER_EMAIL = "shivamBhai12102025@gmail.com"
    SENDER_PASSWORD = "crvm lkjh tgxd qtkx"  # Use an app password if Gmail
    RECEIVER_EMAIL = "malasisatvik16@gmail.com"

    print("\n📧 Sending report via email...")
    emailer = EmailSender(SENDER_EMAIL, SENDER_PASSWORD)
    emailer.send_email(
        to_email=RECEIVER_EMAIL,
        subject="📊 Portfolio Report",
        body="Hi,\n\nPlease find attached the latest portfolio report.\n\n- Automated System",
        # attachment_path=os.path.join(DATA_DIR, "portfolio_report.pdf")
        attachment_path=r"D:\javaProjectsVsCode\python programs\finnhubApi\portfolio_report.pdf"
    )

    print("\n✅ Process completed successfully!")


if __name__ == "__main__":
    main()
