from numpy import log, sqrt, exp
from scipy.stats import norm


class BlackScholes:
    def __init__(self, T: float, K: float, S: float, v: float, r: float, q: float):
        """
        Parameters:
        - T: Time to maturity (in years)
        - K: Strike price
        - S: Spot price
        - v: Volatility (as a percentage, e.g., 20 for 20%)
        - r: Risk-free interest rate (as a percentage)
        - q: Dividend yield (as a percentage)
        """
        self.T = T
        self.K = K
        self.S = S
        self.v = v / 100  # Convert percent to decimal
        self.r = r / 100
        self.q = q / 100

        self._compute_d_values()

    def _compute_d_values(self):
        """
        Compute d1 and d2 values used in pricing formulas.
        """
        if self.v <= 0:
            self.d1 = float('nan')
            self.d2 = float('nan')
        else:
            vol_sqrt_T = self.v * sqrt(self.T)
            numerator = log(self.S / self.K) + self.T * (self.r - self.q + 0.5 * self.v**2)
            self.d1 = numerator / vol_sqrt_T
            self.d2 = self.d1 - vol_sqrt_T

    def calculate_prices(self):
        """
        Calculate and return Black-Scholes call and put prices.
        """
        S, K, T, r, q = self.S, self.K, self.T, self.r, self.q
        d1, d2 = self.d1, self.d2

        call = S * exp(-q * T) * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
        put = K * exp(-r * T) * norm.cdf(-d2) - S * exp(-q * T) * norm.cdf(-d1)

        self.call_price = call
        self.put_price = put

        return call, put

    def vega(self):
        """
        Compute Vega: sensitivity of option price to volatility.
        """
        S, T, q, d1 = self.S, self.T, self.q, self.d1
        return S * exp(-q * T) * norm.pdf(d1) * sqrt(T)
    
    def implied_volatility(self, option_type: str,  market_price: float, iterations: int = 100, tolerance: float = 1e-5) -> tuple:
        """
        Calculate implied volatility using the Newton-Raphson method.
        """
        vol = self.v

        for _ in range(iterations):
            vega = self.vega()
            if vega == 0:
                break  # Prevent division by zero

            self.v = vol
            self._compute_d_values()  # Recalculate d1 and d2 with the new volatility
            call, put = self.calculate_prices()
            option = call if option_type.lower() == 'call' else put
            diff = option - market_price

            
            if abs(diff) < tolerance:
                return option_type, vol
            vol -= (diff) / vega

        return float('nan'), float('nan')  # Return NaN if no convergence
