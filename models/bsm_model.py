from numpy import log, sqrt, exp
from scipy.stats import norm


class BlackScholes:
    def __init__(self, T: float, K: float, S: float, v: float, r: float, q: float):
        """
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

    def _compute_d_values(self) -> None:
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

    def calculate_prices(self) -> tuple:
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

    def vega(self) -> float:
        """
        Compute Vega: sensitivity of option price to volatility.
        """
        S, T, q, d1 = self.S, self.T, self.q, self.d1
        Vega = S * exp(-q * T) * norm.pdf(d1) * sqrt(T)
        return Vega
    
    def gamma(self) -> float:
        """
        Compute Gamma: sensitivity of delta in relation to changes in the underlying asset price.
        """
        S, T, q, d1 = self.S, self.T, self.q, self.d1
        Gamma = norm.pdf(d1) * exp(-q * T) / (S * self.v * sqrt(T))
        return Gamma

    def delta(self) -> tuple:
        """
        Compute Delta: sensitivity of option price to the underlying asset price.
        """
        Call_Delta = exp(-self.q * self.T) * norm.cdf(self.d1)
        Put_Delta = exp(-self.q * self.T) * (Call_Delta - 1)
        return Call_Delta, Put_Delta

    def theta(self) -> tuple:
        """
        Compute Theta: sensitivity of option price to time decay.
        """
        S, K, T, r, q, d1, d2 = self.S, self.K, self.T, self.r, self.q, self.d1, self.d2
        theta_call = (-S * exp(-q * T) * norm.pdf(d1) * self.v / (2 * sqrt(T)) -
                      r * K * exp(-r * T) * norm.cdf(d2) +
                      q * S * exp(-q * T) * norm.cdf(d1))
        theta_put = (-S * exp(-q * T) * norm.pdf(d1) * self.v / (2 * sqrt(T)) +
                     r * K * exp(-r * T) * norm.cdf(-d2) -
                     q * S * exp(-q * T) * norm.cdf(-d1))
        return theta_call, theta_put

    def rho(self) -> tuple:
        """
        Compute Rho: sensitivity of option price to interest rate changes.
        """
        K, T, r, d2 = self.K, self.T, self.r, self.d2
        rho_call = K * T * exp(-r * T) * norm.cdf(d2)
        rho_put = -K * T * exp(-r * T) * norm.cdf(-d2)
        return rho_call, rho_put

    def implied_volatility(self, option_type: str,  market_price: float, iterations: int = 100, tolerance: float = 1e-5) -> float:
        """
        Calculate implied volatility using the Newton-Raphson method.
        """
        vol = self.v

        for _ in range(iterations):
            self.v = vol
            # recalculate d1 and d2 with the new volatility
            self._compute_d_values()
            call, put = self.calculate_prices()

            vega = self.vega()
            if vega == 0:
                # prevent division by zero
                break

            
            option = call if option_type.lower() == 'call' else put
            diff = option - market_price

            # check for convergence
            if abs(diff) < tolerance:
                return vol
            vol -= (diff) / vega

        # return NaN if no convergence
        return float('nan')
