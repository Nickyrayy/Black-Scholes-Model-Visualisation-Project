import streamlit as st

from graphPlots.plot_bsmVsbsml import PlotBsmVsBsml
from graphPlots.plot_option_bsm import PlotOptionBSM
from graphPlots.plot_option_bsml import PlotOptionBSML

@st.cache_data
def generate_bsm_surface(option_type, elevation, rotation, strike_min, strike_max, maturity_min, maturity_max, S, v, r, q):
    """
    Caches the BSM surface plot generation.
    """
    plotter = PlotOptionBSM(strike_min, strike_max, maturity_min, maturity_max, S, v, r, q)
    fig = plotter.plot_option_surface(option_type, elevation, rotation)
    return fig

@st.cache_data
def generate_leland_surface(option_type, elevation, rotation, strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt) :
    """
    Caches the Leland surface plot generation.
    """
    plotter = PlotOptionBSML(strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt)
    fig = plotter.plot_option_surface(option_type, elevation, rotation)
    return fig

@st.cache_data
def generate_bsm_vs_leland_surface(option_type, elevation, rotation, strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt):
    """
    Caches the comparison surface plot generation between BSM and Leland's model.
    """
    plotter = PlotBsmVsBsml(strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt)
    fig = plotter.plot_option_surface(option_type, elevation, rotation)
    return fig