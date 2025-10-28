# the problem here is that whenever i try to open the Connection
# it opens connection for each stock and not for the whole 
# so now i make the whole connection for the all the stocks


# import time
# import pandas as pd
# from websocketClient.websocket_client import websocket_client
# from services.csv_writer import csv_writer

# class latestPrice:
#     def __init__(self, api_key, symbols, csv_path):
#         self.api_key = api_key
#         self.symbols = symbols
#         self.csv_path = csv_path
#         self.csv_writer = csv_writer(filename=self.csv_path)
#         self.client = None

#     def get_latest_tick(self, run_seconds=5):
#         self.client = websocket_client(self.api_key, self.symbols, self.csv_writer)
#         self.client.start()
#         time.sleep(run_seconds)
#         try:
#             self.client.ws.close()
#         except:
#             pass

#         try:
#             df = pd.read_csv(self.csv_path)
#             last_row = df.iloc[-1]
#             return {
#                 "symbol": last_row["Symbol"],
#                 "price": float(last_row["Price"]),
#                 "timestamp": last_row["Time"]
#             }
#         except Exception as e:
#             print("Error reading latest tick:", e)
#             return None





# this new one here, i have made only one connection and get all teh stock price from that
# the csv will only store one line per stock




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

    def get_latest_ticks(self, run_seconds=5):
        """
        Fetch live prices for multiple symbols in one WebSocket connection.
        Returns a dict of {symbol: {"symbol": str, "price": float, "timestamp": str}}
        """
        self.client = websocket_client(self.api_key, self.symbols, self.csv_writer)
        self.client.start()

        # Let it run for a few seconds to gather data
        time.sleep(run_seconds)

        try:
            self.client.ws.close()
        except Exception:
            pass

        # Read combined CSV and extract latest tick per symbol
        results = {}
        try:
            df = pd.read_csv(self.csv_path)
            for symbol in self.symbols:
                sym_data = df[df["Symbol"] == symbol]
                if not sym_data.empty:
                    last_row = sym_data.iloc[-1]
                    results[symbol] = {
                        "symbol": last_row["Symbol"],
                        "price": float(last_row["Price"]),
                        "timestamp": last_row["Time"]
                    }
        except Exception as e:
            print("⚠️ Error reading combined CSV:", e)

        return results
