import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


from functions.computations import get_bsm_prices, get_leland_prices


class PlotBsmVsBsml:
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

    def compute_difference(self, K_val, T_val) -> tuple:
        """ 
        Computes the difference between Leland and Black-Scholes-Merton option prices.
        """

        bsm_call, bsm_put = get_bsm_prices(T_val, K_val, self.S, self.v, self.r, self.q)
        l_call, l_put = get_leland_prices(T_val, K_val, self.S, self.v, self.r, self.q, self.k, self.dt)
        
        call_diff = l_call - bsm_call
        put_diff = l_put - bsm_put

        return call_diff, put_diff

    def plot_option_surface(self, option_type: str, elevation: int, rotation: int):
        """
        Plots the surface of the difference between Leland and BSM option prices.
        """
        # --- initialise the grid for strikes and maturities ---
        strikes = np.linspace(self.strike_min, self.strike_max, 30)
        maturities = np.linspace(self.maturity_min, self.maturity_max, 30)
        K_grid, T_grid = np.meshgrid(strikes, maturities)

        call_diffs, put_diffs = np.vectorize(self.compute_difference)(K_grid, T_grid)

        if option_type == 'Call':
            option_data = call_diffs
            z_label = 'Call Difference'
        elif option_type == 'Put':
            option_data = put_diffs
            z_label = 'Put Difference'
        else:
            raise ValueError(f"Unknown option_type for Leland plot: {option_type}")

        # --- Create the figure ---
        fig = plt.figure(figsize=(8, 8), facecolor="#262730")
        ax = fig.add_subplot(111, projection='3d')
        ax.view_init(elev=elevation, azim=rotation)# type: ignore
        ax.plot_surface(K_grid, T_grid, option_data, cmap='viridis')# type: ignore

        # --- Styling ---
        # labels + titles
        ax.set_xlabel('Strike Price', labelpad=10, color="#FFFFFF")
        ax.set_ylabel('Time to Maturity', labelpad=10, color="#FFFFFF")
        ax.set_zlabel(z_label, labelpad=10, color="#FFFFFF")# type: ignore
        
        # graph colouring
        ax.tick_params(colors='#FFFFFF')
        ax.xaxis._axinfo["grid"]['color'] = "#FFFFFF"# type: ignore
        ax.yaxis._axinfo["grid"]['color'] = "#FFFFFF"# type: ignore
        ax.zaxis._axinfo["grid"]['color'] = "#FFFFFF"# type: ignore
        ax.set_facecolor('#262730')
        fig.patch.set_facecolor("#262730")

        # aspect ratio
        ax.set_box_aspect(None, zoom=0.85) # type: ignore
        
        return fig
