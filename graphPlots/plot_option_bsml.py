import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from models.bsm_leland_model import BlackScholesLeland


class PlotOptionBSML:
    """
    Handles plotting for the Black-Scholes-Leland model.
    """
    def __init__(
        self,
        strike_min: float,
        strike_max: float,
        maturity_min: float,
        maturity_max: float,
        S: float,
        v: float,
        r: float,
        q: float,
        k: float,
        dt: float
    ):
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

    def compute_option_price(self, K_val, T_val):
        """Helper function to calculate Leland prices."""
        model = BlackScholesLeland(T_val, K_val, self.S, self.v, self.r, self.q, self.k, self.dt)
        l_call_price, l_put_price = model.calculate_prices()
        return l_call_price, l_put_price

    def plot_option_surface(self, option_type: str, elevation: int, rotation: int):
        """
        Generates the 3D surface plot for a given option type and view angle.

        Args:
            option_type (str): One of 'Call', 'Put'.
            elevation (int): The elevation angle for the 3D plot.
            rotation (int): The rotation (azimuth) angle for the 3D plot.

        Returns:
            matplotlib.figure.Figure: The generated plot figure.
        """
        strikes = np.linspace(self.strike_min, self.strike_max, 30)
        maturities = np.linspace(self.maturity_min, self.maturity_max, 30)
        K_grid, T_grid = np.meshgrid(strikes, maturities)

        # Vectorize the calculation over the grid
        l_call_p, l_put_p = np.vectorize(self.compute_option_price)(K_grid, T_grid)

        # Select the correct data and set labels
        if option_type == 'Call':
            option_data = l_call_p
            z_label = 'Call Price'
        elif option_type == 'Put':
            option_data = l_put_p
            z_label = 'Put Price'
        else:
            raise ValueError(f"Unknown option_type for Leland plot: {option_type}")

        # --- Create the figure ---
        fig = plt.figure(figsize=(8, 8), facecolor="#262730")
        ax = fig.add_subplot(111, projection='3d')

        # Use the provided elevation and rotation from the sliders
        ax.view_init(elev=elevation, azim=rotation)# type: ignore

        # Plot the surface
        ax.plot_surface(K_grid, T_grid, option_data, cmap='viridis')# type: ignore

        # --- Styling ---
        ax.set_xlabel('Strike Price', labelpad=10, color="#FFFFFF")
        ax.set_ylabel('Time to Maturity', labelpad=10, color="#FFFFFF")
        ax.set_zlabel(z_label, labelpad=10, color="#FFFFFF")# type: ignore
        ax.tick_params(colors='#FFFFFF')
        ax.xaxis._axinfo["grid"]['color'] = "#FFFFFF"# type: ignore
        ax.yaxis._axinfo["grid"]['color'] = "#FFFFFF"# type: ignore
        ax.zaxis._axinfo["grid"]['color'] = "#FFFFFF"# type: ignore
        ax.set_facecolor('#262730')
        fig.patch.set_facecolor("#262730")
        ax.set_box_aspect(None, zoom=0.85) # type: ignore


        # Return the figure object
        return fig
