# restClient/rest_api_client.py
import requests
import csv
import time
from datetime import datetime

class RestAPIClient:
    def __init__(self, api_key, max_attempts=5, backoff_seconds=15):
        self.api_key = api_key
        self.max_attempts = max_attempts
        self.backoff_seconds = backoff_seconds

    def fetch_intraday_candles(self, symbol, interval="30min"):
        url = (
            f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY"
            f"&symbol={symbol}&interval={interval}&apikey={self.api_key}&outputsize=full"
        )

        for attempt in range(1, self.max_attempts + 1):
            try:
                print(f"\n⏳ Attempt {attempt}: Fetching {symbol} {interval} candles...")
                r = requests.get(url)
                data = r.json()

                if "Note" in data:
                    raise Exception(f"Rate limit hit: {data['Note']}")
                elif f"Time Series ({interval})" not in data:
                    raise Exception(f"Unexpected response: {data}")

                time_series = data[f"Time Series ({interval})"]
                print(f"✅ Data fetched successfully ({len(time_series)} rows).")
                return time_series

            except Exception as e:
                print(f"⚠️  Attempt {attempt} failed: {e}")
                if attempt < self.max_attempts:
                    wait_time = self.backoff_seconds * attempt
                    print(f"🔁 Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                else:
                    print("❌ All retries failed.")
                    return {}

    def save_to_csv(self, time_series, filename):
        if not time_series:
            print("⚠️  No data to save.")
            return

        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["time", "open", "high", "low", "close", "volume"])

            for timestamp in sorted(time_series.keys()):
                candle = time_series[timestamp]
                writer.writerow([
                    timestamp,
                    candle["1. open"],
                    candle["2. high"],
                    candle["3. low"],
                    candle["4. close"],
                    candle["5. volume"]
                ])

        print(f"📁 Saved {len(time_series)} rows to '{filename}'.")

# Example usage:
# if __name__ == "__main__":
#     api = RestAPIClient("E7LHCW66U9WKNNSD")
#     candles = api.fetch_intraday_candles("MSFT", "30min")
#     api.save_to_csv(candles, "MSFT_30min_candles.csv")
