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
        self.v = v / 100 # Convert percent to decimal
        self.r = r / 100
        self.q = q / 100
        self.k = k / 100
        self.dt = dt / 252 # Convert trading days to years

        self.call_price = None
        self.put_price = None

        self._compute_d_values()
        self.compute_leland_number()

    def _compute_d_values(self) -> tuple:
        """
        Compute d1 and d2 values used in pricing formulas.
        """
        new_v = self.compute_leland_number()

        if new_v <= 0:
            d1 = float('nan')
            d2 = float('nan')
        else:
            vol_sqrt_T = new_v * sqrt(self.T)
            numerator = log(self.S / self.K) + self.T * (self.r - self.q + 0.5 * new_v**2)
            d1 = numerator / vol_sqrt_T
            d2 = d1 - vol_sqrt_T

        return d1, d2

    def compute_leland_number(self) -> float:
        """
        Compute the Leland number and adjust the volatility accordingly.
        """
        v, k, dt = self.v, self.k, self.dt

        leland_number = sqrt(2 / pi) * (k / (v * sqrt(dt)))
        new_v = sqrt(v**2 * (1 + leland_number))
        return new_v

    def calculate_prices(self) -> tuple:
        """
        Calculate and return Black-Scholes call and put prices adjusted for Leland's model.
        """
        T, K, S, r, q = self.T, self.K, self.S, self.r, self.q,

        new_v = self.compute_leland_number()

        bs_model = BlackScholes(T, K, S, new_v * 100, r * 100, q * 100) # convert back to percentages
        call_price, put_price = bs_model.calculate_prices()

        return call_price, put_price
    
    def vega(self) -> float:
        """
        Compute Vega for the Leland model using the chain rule.
        """
        v = self.v
        if v <= 0:
            return 0.0

        # calculate the adjusted volatility and the Leland Number
        leland_number = sqrt(2 / pi) * (self.k / (v * sqrt(self.dt)))
        v_adj = sqrt(v**2 * (1 + leland_number))

        if v_adj <= 0:
            return 0.0

        # calculate the derivative of the adjustment: d(v_adj) / d(v)
        dv_adj_dv = (v * (1 + 0.5 * leland_number)) / v_adj

        # calculate BSM Vega using the ADJUSTED volatility
        # note: we need a temporary BSM model to get the d1 for the adjusted vol
        temp_bs_model = BlackScholes(self.T, self.K, self.S, v_adj * 100, self.r * 100, self.q * 100)
        bsm_vega_adj = temp_bs_model.vega() # This is dC/dv_adj

        # apply the chain rule
        vega = bsm_vega_adj * dv_adj_dv

        return vega

    def gamma(self) -> float:
        """
        Compute Gamma: sensitivity of delta in relation to changes in the underlying asset price.
        """
        new_v = self.compute_leland_number()
        d1, _ = self._compute_d_values()
        S, T, q = self.S, self.T, self.q
        Gamma = norm.pdf(d1) * exp(-q * T) / (S * new_v * sqrt(T))
        return Gamma

    def delta(self) -> tuple:
        """
        Compute Delta: sensitivity of option price to the underlying asset price.
        """
        d1, _ = self._compute_d_values()
        Call_Delta = exp(-self.q * self.T) * norm.cdf(d1)
        Put_Delta = Call_Delta - exp(-self.q * self.T)
        return Call_Delta, Put_Delta

    def theta(self) -> tuple:
        """
        Compute Theta: sensitivity of option price to time decay.
        """
        d1, d2 = self._compute_d_values()
        new_v = self.compute_leland_number()
        S, K, T, r, q = self.S, self.K, self.T, self.r, self.q
        theta_call = (-S * exp(-q * T) * norm.pdf(d1) * new_v / (2 * sqrt(T)) -
                      r * K * exp(-r * T) * norm.cdf(d2) +
                      q * S * exp(-q * T) * norm.cdf(d1))
        theta_put = (-S * exp(-q * T) * norm.pdf(d1) * new_v / (2 * sqrt(T)) +
                     r * K * exp(-r * T) * norm.cdf(-d2) -
                     q * S * exp(-q * T) * norm.cdf(-d1))
        return theta_call, theta_put

    def rho(self) -> tuple:
        """
        Compute Rho: sensitivity of option price to interest rate changes.
        """
        _, d2 = self._compute_d_values()
        K, T, r = self.K, self.T, self.r
        rho_call = K * T * exp(-r * T) * norm.cdf(d2)
        rho_put = -K * T * exp(-r * T) * norm.cdf(-d2)
        return rho_call, rho_put

    def implied_volatility(self, option_type: str,  market_price: float, iterations: int = 100, tolerance: float = 1e-5) -> float:
        """
        Calculate implied volatility using the Newton-Raphson method for Leland's model.
        """
        input_vol = self.v

        for _ in range(iterations):
            self.v = input_vol

            # recalculate d1 and d2 with the new volatility
            call, put = self.calculate_prices()

            vega = self.vega()
            if vega == 0:
                # prevent division by zero
                break 

            option_price = call if option_type.lower() == 'call' else put
            diff = option_price - market_price

            # check for convergence
            if abs(diff) < tolerance:
                return self.v

            input_vol -= diff / vega

        # return NaN if no convergence
        return float('nan')


        