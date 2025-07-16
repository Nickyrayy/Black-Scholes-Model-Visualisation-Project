from numpy import sqrt, pi
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

    def calculate_prices(self) -> tuple:
        """
        Calculate and return Black-Scholes call and put prices adjusted for Leland's model.

        Args: T, K, S, v, r, q, k, dt

        Returns: Tuple of call and put prices.
        """
        T, K, S, v, r, q, k, dt = self.T, self.K, self.S, self.v, self.r, self.q, self.k, self.dt

        leland_number = sqrt(2 / pi) * (k / (v * sqrt(dt)))
        new_v = sqrt(v**2 * (1 + leland_number))

        bs_model = BlackScholes(T, K, S, new_v * 100, r , q) # convert back to percentages
        call_price, put_price = bs_model.calculate_prices()

        return call_price, put_price