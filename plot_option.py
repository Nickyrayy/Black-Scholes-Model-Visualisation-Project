import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from bsm_model import BlackScholes


class PlotOption:
    def __init__(
            self,
            strike_min: float,
            strike_max: float,
            maturity_min: float,
            maturity_max: float,
            S: float,
            v: float,
            r: float,
            q: float
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
        S = self.S
        v = self.v
        r = self.r
        q = self.q
        model = BlackScholes(T_val, K_val, S, v, r, q)
        call, put = model.calculate_prices()
        return call, put

    def plot_option_surface(self):

        strikes = np.linspace(self.strike_min, self.strike_max, 30)
        maturities = np.linspace(self.maturity_min, self.maturity_max, 30)
        K_grid, T_grid = np.meshgrid(strikes, maturities)

        call_surface, _ = np.vectorize(self.compute_option_price)(K_grid, T_grid)

        fig = plt.figure(figsize=(8, 8), facecolor="#FFFFFF", edgecolor="#FFFFFF")
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(K_grid, T_grid, call_surface, cmap='viridis', color="#3D3D3D37") # type: ignore
        ax.set_xlabel('Strike Price', labelpad=10, color="#FFFFFF")
        ax.set_ylabel('Time to Maturity', labelpad=10, color="#FFFFFF")
        ax.set_zlabel('Call Option Value', labelpad=5, color="#FFFFFF") # type: ignore
        ax.tick_params(colors='#FFFFFF')
        ax.xaxis._axinfo["grid"]['color'] = '#FFFFFF' # type: ignore
        ax.yaxis._axinfo["grid"]['color'] = '#FFFFFF' # type: ignore
        ax.zaxis._axinfo["grid"]['color'] = '#FFFFFF' # type: ignore

        ax.set_box_aspect(None, zoom=0.85) # type: ignore

        #ax.zaxis.set_label_coords(-0.15, 0.5) # type: ignore

        a = st.slider('Elevation', min_value=0, max_value=90, value=20, step=5)
        b = st.slider('Rotation', min_value=0, max_value=360, value=330, step=5)
        ax.view_init(elev=a, azim=b) # type: ignore
        fig.patch.set_facecolor("#262730")
        ax.set_facecolor('#262730') #262730

        #plt.subplots_adjust(left=0.1, right=0.9, top=0.99, bottom=0.1)
        #plt.tight_layout()

        st.pyplot(fig)