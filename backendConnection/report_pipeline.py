import os
from services.email_sender import EmailSender
from RestApi.mainREST import RestAPIClient
from portfolioUtility.latestprice_throughRest import latestprice_throughRest
from portfolioUtility.portfolioCalculator import PortfolioCalculator
from portfolioUtility.reportGeneration import ReportGenerator
from portfolioUtility.hybrid_price_fetcher import fetch_latest_prices

def generate_and_send_report(holdings, receiver_email):
    """
    holdings: dict like {'AAPL': 10, 'MSFT': 20, ...}
    receiver_email: string
    """

    # === CONFIGURATION ===
    REST_API_KEY = "E7LHCW66U9WKNNSD"
    WS_API_KEY = "d3gki79r01qpep678tn0d3gki79r01qpep678tng"
    INTERVAL = "30min"
    DATA_DIR = "data"
    os.makedirs(DATA_DIR, exist_ok=True)

    # === STEP 1: LOAD EXISTING CSVs (or fetch) ===
    print("\n📂 Using existing historical CSV files...")
    historical_data_paths = {}
    for symbol in holdings.keys():
        file_path = os.path.join(DATA_DIR, f"{symbol}_{INTERVAL}.csv")
        if os.path.exists(file_path):
            historical_data_paths[symbol] = file_path
            print(f"✅ Found {symbol} data at {file_path}")
        else:
            print(f"⚠️ Missing CSV for {symbol}: {file_path}")

    # === STEP 2: FETCH LATEST PRICES ===
    print("\n💹 Fetching latest prices (Hybrid)...")
    live_prices = fetch_latest_prices(holdings.keys(), WS_API_KEY, REST_API_KEY, DATA_DIR, interval=INTERVAL)

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
    report_path = os.path.join(DATA_DIR, "portfolio_report.pdf")
    report = ReportGenerator(report_path)
    report.generate(metrics, holdings)

    # === STEP 5: EMAIL REPORT ===
    print("\n📧 Sending report via email...")
    SENDER_EMAIL = "shivamBhai12102025@gmail.com"
    SENDER_PASSWORD = "crvm lkjh tgxd qtkx"  # App password recommended

    emailer = EmailSender(SENDER_EMAIL, SENDER_PASSWORD)
    emailer.send_email(
        to_email=receiver_email,
        subject="📊 Portfolio Report",
        body="Hi,\n\nPlease find attached the latest portfolio report.\n\n- Portfolio Analyzer",
        attachment_path=report_path
    )

    print("\n✅ Process completed successfully!")
