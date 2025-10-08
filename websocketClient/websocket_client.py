import json
import websocket
import threading
from services.csv_writer import csv_writer
from modal.stock_data import stock_data

class websocket_client:
    """
    WebSocket client to Finnhub.
    """
    def __init__(self, api_key: str, symbols: list, csv_writer: csv_writer):
        self.api_key = api_key
        self.symbols = symbols
        self.csv_writer = csv_writer
        self.ws = None

    def on_open(self, ws):
        print("Connected to Finnhub WebSocket")
        for symbol in self.symbols:
            msg = json.dumps({"type": "subscribe", "symbol": symbol})
            ws.send(msg)
            print(f"Subscribed: {symbol}")

    def on_message(self, ws, message):
        data = json.loads(message)
        if "data" in data:
            for t in data["data"]:
                update = stock_data(
                    price=t["p"],
                    symbol=t["s"],
                    time=t["t"],
                    volume=t["v"]
                )
                self.csv_writer.write(update)

    def on_close(self, ws, close_status_code, close_msg):
        print(f"Connection closed: {close_status_code} - {close_msg}")

    def on_error(self, ws, error):
        print(f"WebSocket error: {error}")

    def start(self):
        url = f"wss://ws.finnhub.io?token={self.api_key}"
        self.ws = websocket.WebSocketApp(
            url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_close=self.on_close,
            on_error=self.on_error
        )
        # Run in a separate thread so it doesn't block
        wst = threading.Thread(target=self.ws.run_forever)
        wst.daemon = True
        wst.start()
