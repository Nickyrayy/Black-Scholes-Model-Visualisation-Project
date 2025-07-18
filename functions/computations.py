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
def get_implied_volatility(T, K, S, v, r, q, k, dt, option_type, market_price, model_type):
    """
    Caches the implied volatility calculation.
    """
    if model_type == "Black-Scholes":
        bs_model = BlackScholes(T, K, S, v, r, q)
        return bs_model.implied_volatility(option_type, market_price)
    
    else:
        bsml_model = BlackScholesLeland(T, K, S, v, r, q, k, dt)
        return bsml_model.implied_volatility(option_type, market_price)

@st.cache_data
def get_vega(T, K, S, v, r, q, option_type, market_price):
    """
    Caches the Vega calculation.
    """
    bs_model = BlackScholes(T, K, S, v, r, q)
    return bs_model.vega(option_type, market_price)

@st.cache_data
def get_gamma(T, K, S, v, r, q, option_type, market_price):
    """
    Caches the Gamma calculation.
    """
    bs_model = BlackScholes(T, K, S, v, r, q)
    return bs_model.gamma(option_type, market_price)
