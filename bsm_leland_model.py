from numpy import log, sqrt, exp, pi
from scipy.stats import norm


class BlackScholesLeland:
    def __init__(
        self,
        T: float,
        K: float,
        S: float,
        v: float,
        r: float,
        q: float,
        k: float,
        dt: float,
    ):
        self.T = T
        self.K = K
        self.S = S
        self.v = v / 100
        self.r = r / 100
        self.q = q / 100
        self.k = k / 100
        self.dt = dt

    def calculate_prices(
        self,
    ):
        T = self.T # Time to expiry
        K = self.K # Strike price
        S = self.S # Stock price
        v = self.v # Volatilty
        r = self.r # Risk-free interest rate
        q = self.q # Dividend yield
        k = self.k # Roundtrip transaction cost rate per unit dollar of transaction
        dt = self.dt # Delta t, the time between hedging adjustment
        
        V = (
            (v * (1 + k * sqrt(2/pi))) /
            (sqrt(v * sqrt(dt)))
            )
                              # Leland variation should be caclulated in trading days
                            # T represents the workings day from purchase to the *day before* expiry
        d1 = (
        (log(S / K) + T * (r - q + 0.5 * V ** 2)) / 
        (V * sqrt(T))
        )
        
        d2 = d1 - V * sqrt(T)

        cash_call_price = (
        (1 + (k/2)) * S * exp(-q * T) * norm.cdf(d1) - 
        K * exp(-(r * T)) * norm.cdf(d2)
        )

        cash_put_price = (
        K * exp(-(r * T)) * norm.cdf(-d2) - 
        (1-(k/2)) * S * exp(-q * T) * norm.cdf(-d1) + 
        (k/2) * S * exp(-(q) * T)
        )

        stock_call_price = (
        (k/2) * S * exp(-q * T) +
        (1-(k/2)) * S * exp(-q * T) * norm.cdf(d1) - 
        K * exp(-(r * T)) * norm.cdf(d2)
        )

        stock_put_price = (
        K * exp(-(r * T)) * norm.cdf(-d2) - 
        (1-(k/2)) * S * exp(-q * T) * norm.cdf(-d1)
        )

        self.cash_call_price = cash_call_price
        self.cash_put_price = cash_put_price
        self.stock_call_price = stock_call_price
        self.stock_put_price = stock_put_price

        return cash_call_price, cash_put_price, stock_call_price, stock_put_price