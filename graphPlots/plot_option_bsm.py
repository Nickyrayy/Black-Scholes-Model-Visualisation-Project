import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from models.bsm_model import BlackScholes


class PlotOptionBSM:
    """
    Handles plotting for the standard Black-Scholes model.
    """
    def __init__(self, strike_min: float, strike_max: float, maturity_min: float, maturity_max: float, S: float, v: float, r: float, q: float):

        self.strike_min = strike_min
        self.strike_max = strike_max
        self.maturity_min = maturity_min
        self.maturity_max = maturity_max
        self.S = S
        self.v = v
        self.q = q
        self.r = r

    def compute_option_price(self, K_val, T_val) -> tuple:
        """
        Helper function to calculate BSM prices.
        """
        model = BlackScholes(T_val, K_val, self.S, self.v, self.r, self.q)
        call_price, put_price = model.calculate_prices()
        return call_price, put_price

    def plot_option_surface(self, option_type: str, elevation: int, rotation: int):
        """
        Generates the 3D surface plot for a given option type.
        """
        # --- initialise the grid for strikes and maturities ---
        strikes = np.linspace(self.strike_min, self.strike_max, 30)
        maturities = np.linspace(self.maturity_min, self.maturity_max, 30)
        K_grid, T_grid = np.meshgrid(strikes, maturities)

        call_prices, put_prices = np.vectorize(self.compute_option_price)(K_grid, T_grid)

        if option_type == 'Call':
            option_data = call_prices
            z_label = 'Call Option Price'  
        elif option_type == 'Put':
            option_data = put_prices
            z_label = 'Put Option Price'
        else:
            raise ValueError(f"Unknown option_type for BSM plot: {option_type}")

        # --- Create the figure ---
        fig = plt.figure(figsize=(8, 8), facecolor="#FFFFFF", edgecolor="#262730")
        ax = fig.add_subplot(111, projection='3d')
        ax.view_init(elev=elevation, azim=rotation)# type: ignore
        ax.plot_surface(K_grid, T_grid, option_data, cmap='viridis')# type: ignore

        # --- Styling ---
        # labels + titles
        ax.set_xlabel('Strike Price', labelpad=10, color="#FFFFFF")
        ax.set_ylabel('Time to Maturity', labelpad=10, color="#FFFFFF")
        ax.set_zlabel(z_label, labelpad=10, color="#FFFFFF")# type: ignore
        
        # graph colouring
        ax.tick_params(colors="#FFFFFF")
        ax.xaxis._axinfo["grid"]['color'] = "#FFFFFF"# type: ignore
        ax.yaxis._axinfo["grid"]['color'] = "#FFFFFF"# type: ignore
        ax.zaxis._axinfo["grid"]['color'] = "#FFFFFF"# type: ignore
        ax.set_facecolor("#262730")
        fig.patch.set_facecolor("#262730")

        # aspect ratio
        ax.set_box_aspect(None, zoom=0.85) # type: ignore

        return fig
