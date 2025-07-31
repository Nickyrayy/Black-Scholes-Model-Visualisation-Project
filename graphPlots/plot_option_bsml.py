import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from models.bsm_leland_model import BlackScholesLeland


class PlotOptionBSML:
    """
    Handles plotting for the Black-Scholes-Leland model.
    """
    def __init__(self, strike_min: float, strike_max: float, maturity_min: float, maturity_max: float, S: float, v: float, r: float, q: float, k: float, dt: float):
        
        self.strike_min = strike_min
        self.strike_max = strike_max
        self.maturity_min = maturity_min
        self.maturity_max = maturity_max
        self.S = S
        self.v = v
        self.q = q
        self.r = r
        self.k = k
        self.dt = dt

    def compute_option_price(self, K_val, T_val) -> tuple:
        """
        Helper function to calculate Leland prices.
        """
        model = BlackScholesLeland(T_val, K_val, self.S, self.v, self.r, self.q, self.k, self.dt)
        l_call_price, l_put_price = model.calculate_prices()
        return l_call_price, l_put_price

    def plot_option_surface(self, option_type: str, elevation: int, rotation: int):
        """
        Generates the 3D surface plot for a given option type and view angle.
        """
        # --- initialise the grid for strikes and maturities ---
        strikes = np.linspace(self.strike_min, self.strike_max, 30)
        maturities = np.linspace(self.maturity_min, self.maturity_max, 30)
        K_grid, T_grid = np.meshgrid(strikes, maturities)

        l_call_p, l_put_p = np.vectorize(self.compute_option_price)(K_grid, T_grid)

        if option_type == 'Call':
            option_data = l_call_p
            z_label = 'Call Price'
        elif option_type == 'Put':
            option_data = l_put_p
            z_label = 'Put Price'
        else:
            raise ValueError(f"Unknown option_type for Leland plot: {option_type}")

        # --- Create the figure ---
        fig = plt.figure(figsize=(8, 8), facecolor="#6b0000ff")
        ax = fig.add_subplot(111, projection='3d')
        ax.view_init(elev=elevation, azim=rotation)# type: ignore
        ax.plot_surface(K_grid, T_grid, option_data, cmap='viridis')# type: ignore

        # --- Styling ---
        # labels + titles
        ax.set_xlabel('Strike Price', labelpad=10, color="#6b0000ff")
        ax.set_ylabel('Time to Maturity', labelpad=10, color="#6b0000ff")
        ax.set_zlabel(z_label, labelpad=10, color="#6b0000ff")# type: ignore

        # ticks
        ax.tick_params(colors="#6b0000ff")

        # grid lines
        ax.xaxis._axinfo["grid"]['color'] = "#6b0000ff"# type: ignore
        ax.yaxis._axinfo["grid"]['color'] = "#6b0000ff"# type: ignore
        ax.zaxis._axinfo["grid"]['color'] = "#6b0000ff"# type: ignore

        # background
        ax.set_facecolor("#fff7e6ff")
        # border
        fig.patch.set_facecolor("#fff7e6ff")

        # aspect ratio
        ax.set_box_aspect(None, zoom=0.85) # type: ignore

        return fig
