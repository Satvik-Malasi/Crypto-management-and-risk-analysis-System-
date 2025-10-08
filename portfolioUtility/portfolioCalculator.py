# portfolio_utils/portfolio_calculator.py

import pandas as pd
import numpy as np

class PortfolioCalculator:
    def __init__(self, holdings, historical_data_paths, live_prices):
        """
        holdings: dict of {symbol: quantity}
        historical_data_paths: dict of {symbol: csv_path_from_rest_api}
        live_prices: dict of {symbol: current_price_from_websocket}
        """
        self.holdings = holdings
        self.historical_data_paths = historical_data_paths
        self.live_prices = live_prices
        self.data = {}
        self.returns = {}
        self.metrics = {}

    def load_data(self):
        for symbol, path in self.historical_data_paths.items():
            df = pd.read_csv(path)
            df["close"] = df["close"].astype(float)
            df = df.sort_values("time")
            self.data[symbol] = df
        return self

    def compute_returns(self):
        for symbol, df in self.data.items():
            df["return"] = df["close"].pct_change()
            self.returns[symbol] = df["return"].dropna()
        return self

    def portfolio_weights(self):
        values = {s: self.holdings[s] * self.live_prices[s] for s in self.holdings}
        total_value = sum(values.values())
        weights = {s: v / total_value for s, v in values.items()}
        return weights, total_value

    def portfolio_volatility(self, weights):
        returns_df = pd.DataFrame(self.returns)
        cov_matrix = returns_df.cov()
        w = np.array([weights[s] for s in returns_df.columns])
        portfolio_vol = np.sqrt(np.dot(w.T, np.dot(cov_matrix, w))) * np.sqrt(252)
        return portfolio_vol

    def max_drawdown(self, symbol):
        df = self.data[symbol]
        df["cum_return"] = (1 + df["return"]).cumprod()
        rolling_max = df["cum_return"].cummax()
        drawdown = (df["cum_return"] - rolling_max) / rolling_max
        return drawdown.min()

    def value_at_risk(self, symbol, confidence=0.95):
        returns = self.returns[symbol]
        var = np.percentile(returns, (1 - confidence) * 100)
        return var

    def compute_portfolio_metrics(self):
        weights, total_value = self.portfolio_weights()

        volatility = self.portfolio_volatility(weights)
        max_dd = {s: self.max_drawdown(s) for s in self.data}
        var = {s: self.value_at_risk(s) for s in self.data}

        initial_value = sum(
            self.holdings[s] * self.data[s]["close"].iloc[0] for s in self.holdings
        )
        profit_loss = total_value - initial_value
        growth = (total_value / initial_value) - 1

        self.metrics = {
            "portfolio_value": total_value,
            "profit_loss": profit_loss,
            "growth": growth,
            "volatility": volatility,
            "max_drawdown": max_dd,
            "value_at_risk": var,
        }
        return self.metrics
