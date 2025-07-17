from numpy import sqrt, pi, log, exp
from scipy.stats import norm
from models.bsm_model import BlackScholes 


class BlackScholesLeland:
    def __init__(self, T: float, K: float, S: float, v: float, r: float, q: float, k: float, dt: float,):
        """
        Parameters:
        - T: Time to maturity (in years)
        - K: Strike price
        - S: Spot price
        - v: Volatility (as a percentage, e.g., 20 for 20%)
        - r: Risk-free interest rate (as a percentage)
        - q: Dividend yield (as a percentage)
        - k: Roundtrip transaction cost rate per unit dollar of transaction (as a percentage)
        - dt: Delta t, the time between hedging adjustment (in trading days)
        """

        self.T = T
        self.K = K
        self.S = S
        self.v = v / 100
        self.r = r
        self.q = q
        self.k = k / 100
        self.dt = dt / 252

        self.call_price = None
        self.put_price = None

        self._compute_d_values()
        self.compute_leland_number()

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

    def compute_leland_number(self):
        v, k, dt = self.v, self.k, self.dt

        leland_number = sqrt(2 / pi) * (k / (v * sqrt(dt)))
        new_v = sqrt(v**2 * (1 + leland_number))
        return new_v

    def calculate_prices(self) -> tuple:
        """
        Calculate and return Black-Scholes call and put prices adjusted for Leland's model.

        Args: T, K, S, v, r, q, k, dt

        Returns: Tuple of call and put prices.
        """
        T, K, S, r, q = self.T, self.K, self.S, self.r, self.q,

        new_v = self.compute_leland_number()

        bs_model = BlackScholes(T, K, S, new_v * 100, r , q) # convert back to percentages
        call_price, put_price = bs_model.calculate_prices()

        return call_price, put_price
    
    def vega(self, option_type, market_price):
        """
        Compute Vega: sensitivity of option price to volatility.
        """
        S, T, q, d1 = self.S, self.T, self.q, self.d1
        Vega = S * exp(-q * T) * norm.pdf(d1) * sqrt(T)
        Vega /= 100 # Vega is often expressed per 1% change in volatility
        return option_type, Vega
    
    def implied_volatility(self, option_type: str,  market_price: float, iterations: int = 100, tolerance: float = 1e-5) -> tuple:
        """
        Calculate implied volatility using the Newton-Raphson method.
        """
        vol = self.compute_leland_number()

        for _ in range(iterations):
            vega = self.vega(option_type, market_price)
            if vega == 0:
                break  # Prevent division by zero

            vol = self.compute_leland_number()
            self._compute_d_values()  # Recalculate d1 and d2 with the new volatility
            call, put = self.calculate_prices()
            option = call if option_type.lower() == 'call' else put
            diff = option - market_price

            
            if abs(diff) < tolerance:
                return option_type, vol
            vol -= (diff) / vega

        return float('nan'), float('nan')  # Return NaN if no convergence



        