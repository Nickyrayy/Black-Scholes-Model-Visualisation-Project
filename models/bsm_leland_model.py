from numpy import sqrt, pi
from models.bsm_model import BlackScholes 


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
        self.dt = dt / 252

        self.call_price = None
        self.put_price = None

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

        leland_number = sqrt(2 / pi) * (k / (v * sqrt(dt)))
        new_v = sqrt(v**2 * (1 + leland_number))

        bs_model = BlackScholes(T, K, S, new_v * 100, r * 100, q * 100) # convert back to percentages
        call_price, put_price = bs_model.calculate_prices()

        return call_price, put_price