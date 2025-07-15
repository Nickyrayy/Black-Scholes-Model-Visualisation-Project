import streamlit as st

from models.bsm_model import BlackScholes
from graphPlots.plot_option_bsm import PlotOptionBSM
from graphPlots.plot_option_bsml import PlotOptionBSML
from models.bsm_leland_model import BlackScholesLeland

@st.cache_data
def get_bsm_prices(T, K, S, v, r, q):
    """
    Caches the Black-Scholes price calculation.
    """
    bs_model = BlackScholes(T, K, S, v, r, q)
    return bs_model.calculate_prices()

@st.cache_data
def generate_bsm_surface(option_type, elevation, rotation, strike_min, strike_max, maturity_min, maturity_max, S, v, r, q):
    """
    Caches the BSM surface plot generation.
    """
    plotter = PlotOptionBSM(strike_min, strike_max, maturity_min, maturity_max, S, v, r, q)
    fig = plotter.plot_option_surface(option_type, elevation, rotation)
    return fig

@st.cache_data
def get_leland_prices(T, K, S, v, r, q, k, dt):
    """
    Caches the Leland price calculation.
    """
    bsml_model = BlackScholesLeland(T, K, S, v, r, q, k, dt)
    return bsml_model.calculate_prices()

@st.cache_data
def generate_leland_surface(option_type, elevation, rotation, strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt):
    """
    Caches the Leland surface plot generation.
    """
    plotter = PlotOptionBSML(strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt)
    fig = plotter.plot_option_surface(option_type, elevation, rotation)
    return fig

@st.cache_data
def get_implied_volatility(T, K, S, v, r, q, option_type, market_price):
    """
    Caches the implied volatility calculation.
    """
    bs_model = BlackScholes(T, K, S, v, r, q)
    return bs_model.implied_volatility(option_type, market_price)
