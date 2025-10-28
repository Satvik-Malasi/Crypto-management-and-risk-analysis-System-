#  the fetching of the stock is making multiple connections
# this is why commmented


# import os
# import pandas as pd
# from portfolioUtility.latestprice_throughRest import latestprice_throughRest
# from portfolioUtility.latestPrice import latestPrice

# def fetch_latest_prices(symbols, api_key, data_dir, interval="30min"):
#     """
#     Fetch latest prices using:
#     1️⃣ WebSocket (Finnhub)
#     2️⃣ CSV fallback (last candle)
#     3️⃣ REST fallback (Finnhub REST API)
#     """
#     live_prices = {}

#     for symbol in symbols:
#         print(f"\n💹 Fetching live price for {symbol}...")

#         csv_path = os.path.join(data_dir, f"{symbol}_{interval}.csv")  # historical candles
#         ws_csv_path = os.path.join(data_dir, f"{symbol}_live.csv")    # live ticks

#         # 1️⃣ Try WebSocket first
#         ws_fetcher = latestPrice(api_key, [symbol], ws_csv_path)
#         tick = ws_fetcher.get_latest_tick(run_seconds=5)

#         # 2️⃣ CSV fallback (if WebSocket fails)
#         if not tick:
#             print(f"💤 No WebSocket data for {symbol}, trying CSV fallback...")
#             if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
#                 try:
#                     df = pd.read_csv(csv_path)
#                     last_row = df.iloc[-1]
#                     tick = {
#                         "symbol": symbol,
#                         "price": float(last_row["close"]),
#                         "timestamp": last_row["time"],
#                         "volume": float(last_row.get("volume", 0))
#                     }
#                     print(f"📄 Used last saved CSV close price for {symbol}: ${tick['price']}")
#                 except Exception as e:
#                     print(f"⚠️ Could not read from CSV for {symbol}: {e}")
#             else:
#                 print(f"⚠️ No CSV file found for {symbol}, trying REST...")

#         # 3️⃣ REST fallback
#         if not tick:
#             rest_fetcher = latestprice_throughRest(api_key, [symbol], ws_csv_path)
#             tick = rest_fetcher.get_latest_tick()
#             if tick:
#                 print(f"🌐 Used REST API for {symbol}: ${tick['price']}")
#             else:
#                 print(f"❌ Could not fetch {symbol} from any source.")
#                 tick = {"symbol": symbol, "price": 0, "timestamp": None, "volume": 0}

#         live_prices[symbol] = tick["price"]

#     return live_prices




import os
import pandas as pd
from portfolioUtility.latestPrice import latestPrice
from portfolioUtility.latestprice_throughRest import latestprice_throughRest


def fetch_latest_prices(symbols, ws_api_key, rest_api_key, data_dir,interval="30min"):
    """
    Hybrid price fetcher:
    - Tries to fetch live data via a single WebSocket connection for all symbols.
    - Falls back to REST or local CSV if WebSocket fails or returns no data.
    """
    # === 1st WebSocket Attempt ===
    print("\n🔌 Trying to fetch live prices via WebSocket...")
    combined_csv = os.path.join(data_dir, "live_combined.csv")
    ws_fetcher = latestPrice(ws_api_key, list(symbols), combined_csv)
    ws_results = ws_fetcher.get_latest_ticks(run_seconds=5)

    live_prices = {}

    # === 2nd Process each symbol ===
    for symbol in symbols:
        tick = ws_results.get(symbol) if ws_results else None

        if tick and tick["price"] > 0:
            print(f"✅ [WS] {symbol} = ${tick['price']}")
            live_prices[symbol] = tick["price"]
            continue

    #     # --- trying the 3rd attempt If WebSocket not available ---
    #     print(f"💤 No WebSocket data for {symbol}, trying REST...")

    #     try:
    #         rest_fetcher = latestprice_throughRest(rest_api_key, [symbol], os.path.join(data_dir, f"{symbol}_live.csv"))
    #         tick = rest_fetcher.get_latest_tick()

    #         if tick and tick["price"] > 0:
    #             print(f"✅ [REST] {symbol} = ${tick['price']}")
    #             live_prices[symbol] = tick["price"]
    #             continue
    #     except Exception as e:
    #         print(f"⚠️ REST fetch failed for {symbol}: {e}")

    #     # --- If both fail, read last known from historical CSV ---
    #     hist_path = os.path.join(data_dir, f"{symbol}_30min.csv")
    #     if os.path.exists(hist_path):
    #         try:
    #             df = pd.read_csv(hist_path)
    #             last_row = df.iloc[-1]
    #             live_prices[symbol] = float(last_row["close"])
    #             print(f"📁 [Local CSV] {symbol} = ${live_prices[symbol]} (from historical data)")
    #         except Exception as e:
    #             print(f"⚠️ Could not read fallback CSV for {symbol}: {e}")
    #             live_prices[symbol] = 0
    #     else:
    #         print(f"❌ No data available for {symbol}")
    #         live_prices[symbol] = 0

    # print("\n✅ Live price fetching complete.\n")
    # return live_prices



            # --- If WebSocket data not available ---
        print(f"💤 No WebSocket data for {symbol}, trying historical CSV...")

        # --- Try historical data first ---
        hist_path = os.path.join(data_dir, f"{symbol}_{interval}.csv")
        if os.path.exists(hist_path):
            try:
                df = pd.read_csv(hist_path)
                last_row = df.iloc[-1]
                live_prices[symbol] = float(last_row["close"])
                print(f"📁 [Local CSV] {symbol} = ${live_prices[symbol]} (from historical data)")
                continue
            except Exception as e:
                print(f"⚠️ Could not read fallback CSV for {symbol}: {e}")

        # --- If historical also fails, try REST API ---
        print(f"💤 Historical CSV missing or failed for {symbol}, trying REST...")

        try:
            rest_fetcher = latestprice_throughRest(
                rest_api_key,
                [symbol],
                os.path.join(data_dir, f"{symbol}_live.csv")
            )
            tick = rest_fetcher.get_latest_tick()

            if tick and tick["price"] > 0:
                print(f"✅ [REST] {symbol} = ${tick['price']}")
                live_prices[symbol] = tick["price"]
                continue
        except Exception as e:
            print(f"⚠️ REST fetch failed for {symbol}: {e}")
            live_prices[symbol] = 0
    print("\n✅ Live price fetching complete.\n")
    return live_prices