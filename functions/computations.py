import streamlit as st

from models.bsm_model import BlackScholes
from models.bsm_leland_model import BlackScholesLeland

@st.cache_data
def get_bsm_prices(T, K, S, v, r, q):
    """
    Caches the Black-Scholes price calculation.
    """
    bs_model = BlackScholes(T, K, S, v, r, q)
    return bs_model.calculate_prices()

@st.cache_data
def get_leland_prices(T, K, S, v, r, q, k, dt):
    """
    Caches the Leland price calculation.
    """
    bsml_model = BlackScholesLeland(T, K, S, v, r, q, k, dt)
    return bsml_model.calculate_prices()


@st.cache_data
def get_implied_volatility(T, K, S, v, r, q, option_type, market_price):
    """
    Caches the implied volatility calculation.
    """
    bs_model = BlackScholes(T, K, S, v, r, q)
    return bs_model.implied_volatility(option_type, market_price)
