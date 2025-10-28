# import requests
# import time

# class rest_through_finnhub:
    # def __init__(self, api_key):
    #     self.api_key = api_key
    #     self.base_url = "https://finnhub.io/api/v1/quote"

    # def fetch_quote(self, symbol):
    #     """
    #     Fetches the latest quote for a given symbol (stock or crypto).
    #     Returns a dict with symbol, price, volume, and timestamp.
    #     """
    #     try:
    #         url = f"{self.base_url}?symbol={symbol}&token={self.api_key}"
    #         response = requests.get(url)
    #         data = response.json()

    #         if "c" not in data or data["c"] == 0:
    #             print(f"⚠️ No valid data for {symbol}")
    #             return None

    #         return {
    #             "symbol": symbol,
    #             "price": data["c"],
    #             "volume": data.get("v", 0),
    #             "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    #         }

    #     except Exception as e:
    #         print(f"❌ REST fetch error for {symbol}: {e}")
    #         return None





import requests
import time

class rest_through_finnhub:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://finnhub.io/api/v1/quote"

    def fetch_quote(self, symbol):
        """
        Fetches the latest quote for a given symbol (stock or crypto).
        Returns a dict with symbol, price, volume, and timestamp.
        Handles closed market by using previous close if no current price.
        """
        try:
            url = f"{self.base_url}?symbol={symbol}&token={self.api_key}"
            response = requests.get(url)
            data = response.json()

            # Use current price if available; otherwise fallback to previous close
            if "c" not in data:
                print(f"❌ No data for {symbol}")
                return None

            price = data["c"] if data["c"] != 0 else data.get("pc", 0)
            if price == 0:
                print(f"⚠️ No valid price for {symbol}")
                return None

            return {
                "symbol": symbol,
                "price": price,
                "high": data.get("h", 0),
                "low": data.get("l", 0),
                "open": data.get("o", 0),
                "previous_close": data.get("pc", 0),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }

        except Exception as e:
            print(f"❌ REST fetch error for {symbol}: {e}")
            return None

# ========================
# Example main usage
# ========================
# if __name__ == "__main__":
#     API_KEY = "YOUR_KEY"  # replace with your Finnhub API key
#     finnhub_client = rest_through_finnhub(API_KEY)

#     symbols = ["AAPL", "MSFT", "TSLA"]
#     for sym in symbols:
#         quote = finnhub_client.fetch_quote(sym)
#         print(quote)
