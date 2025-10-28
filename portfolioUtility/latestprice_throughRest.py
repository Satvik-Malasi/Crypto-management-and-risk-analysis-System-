import pandas as pd
from finnhubRestApi.rest_through_finnhub import rest_through_finnhub
from services.csv_writer import csv_writer

class latestprice_throughRest:
    def __init__(self, api_key, symbols, csv_path):
        self.api_key = api_key
        self.symbols = symbols
        self.csv_path = csv_path
        self.csv_writer = csv_writer(filename=self.csv_path)
        self.client = rest_through_finnhub(api_key)

    def get_latest_tick(self):
        all_data = []

        for symbol in self.symbols:
            latest = self.client.fetch_quote(symbol)
            if latest:
                # write to CSV
                self.csv_writer.write(
                    type("stock_data", (), latest)  # mimic object
                )
                all_data.append(latest)
                print(f"✅ Saved {symbol} at ${latest['price']}")

        # return last fetched record
        if all_data:
            last = all_data[-1]
            return {
                "symbol": last["symbol"],
                "price": last["price"],
                "timestamp": last["timestamp"]
            }
        else:
            print("⚠️ No data fetched.")
            return None
