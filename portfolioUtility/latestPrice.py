import time
import pandas as pd
from websocketClient.websocket_client import websocket_client
from services.csv_writer import csv_writer

class latestPrice:
    def __init__(self, api_key, symbols, csv_path):
        self.api_key = api_key
        self.symbols = symbols
        self.csv_path = csv_path
        self.csv_writer = csv_writer(filename=self.csv_path)
        self.client = None

    def get_latest_tick(self, run_seconds=5):
        self.client = websocket_client(self.api_key, self.symbols, self.csv_writer)
        self.client.start()
        time.sleep(run_seconds)
        try:
            self.client.ws.close()
        except:
            pass

        try:
            df = pd.read_csv(self.csv_path)
            last_row = df.iloc[-1]
            return {
                "symbol": last_row["Symbol"],
                "price": float(last_row["Price"]),
                "timestamp": last_row["Time"]
            }
        except Exception as e:
            print("Error reading latest tick:", e)
            return None
