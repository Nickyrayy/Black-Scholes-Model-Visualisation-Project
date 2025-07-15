import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# This model is assumed to be in the models/ folder
from models.bsm_model import BlackScholes


class PlotOptionBSM:
    """
    Handles plotting for the standard Black-Scholes model.
    This version is designed to be non-interactive.
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
    ):
        self.strike_min = strike_min
        self.strike_max = strike_max
        self.maturity_min = maturity_min
        self.maturity_max = maturity_max
        self.S = S
        self.v = v
        self.q = q
        self.r = r

    def compute_option_price(self, K_val, T_val):
        """Helper function to calculate BSM prices."""
        model = BlackScholes(T_val, K_val, self.S, self.v, self.r, self.q)
        call_price, put_price = model.calculate_prices()
        return call_price, put_price

    def plot_option_surface(self, option_type: str):
        """
        Generates the 3D surface plot for a given option type.
        
        Args:
            option_type (str): Either "call" or "put".

        Returns:
            matplotlib.figure.Figure: The generated plot figure.
        """
        strikes = np.linspace(self.strike_min, self.strike_max, 30)
        maturities = np.linspace(self.maturity_min, self.maturity_max, 30)
        K_grid, T_grid = np.meshgrid(strikes, maturities)

        # Vectorize the calculation over the grid
        call_prices, put_prices = np.vectorize(self.compute_option_price)(K_grid, T_grid)

        # Select the correct data and set labels
        if option_type == 'call':
            option_data = call_prices
            z_label = 'Call Option Price'
            rotation = 330  # Default rotation for calls
        elif option_type == 'put':
            option_data = put_prices
            z_label = 'Put Option Price'
            rotation = 230  # Default rotation for puts
        else:
            raise ValueError(f"Unknown option_type for BSM plot: {option_type}")

        # --- Create the figure ---
        fig = plt.figure(figsize=(8, 8), facecolor="#262730")
        ax = fig.add_subplot(111, projection='3d')

        # Set fixed view angles for non-interactive plot
        ax.view_init(elev=20, azim=rotation) # type: ignore

        # Plot the surface
        ax.plot_surface(K_grid, T_grid, option_data, cmap='viridis')# type: ignore

        # --- Styling ---
        ax.set_xlabel('Strike Price', labelpad=10, color="#FFFFFF")
        ax.set_ylabel('Time to Maturity', labelpad=10, color="#FFFFFF")
        ax.set_zlabel(z_label, labelpad=10, color="#FFFFFF")# type: ignore
        ax.tick_params(colors='#FFFFFF')
        ax.xaxis._axinfo["grid"]['color'] = '#3D3D3D'# type: ignore
        ax.yaxis._axinfo["grid"]['color'] = '#3D3D3D'# type: ignore
        ax.zaxis._axinfo["grid"]['color'] = '#3D3D3D'# type: ignore
        ax.set_facecolor('#262730')

        # Return the figure object instead of plotting it
        return fig
