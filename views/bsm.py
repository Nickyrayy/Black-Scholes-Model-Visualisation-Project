import streamlit as st
import sys
sys.path.append('views')

from computations import (
    get_bsm_prices,
    generate_bsm_surface,
    get_leland_prices,
    generate_leland_surface,
    get_implied_volatility
)
from helper import display_option_surface

st.set_page_config(
    page_title="Black-Scholes Model",
    page_icon=":material/functions:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.title("Model Parameters")

    st.subheader("Required Inputs")
    
    S = st.number_input("Current Asset Price $", min_value=0.0, value=100.0, step=5.0, format="%0.2f", key="S")
    K = st.number_input("Current strike Price $", min_value=0.0, value=100.0, step=5.0, format="%0.2f", key="K")
    T = st.number_input("Time to expiration (Annualised)", min_value=0.0, value=1.0, step=0.1, format="%0.2f", key="T")
    r = st.number_input("Risk-Free Interest Rate % (Annualised)", min_value=0.0, value=5.0, step=0.05, format="%0.2f", key="r")
    v = st.number_input("Volatility %", min_value=0.00, value=20.0, step=0.01, format="%0.2f", key="v")
    
    st.divider()

    st.subheader("Optional Inputs")

    q = st.number_input("Expected Dividend Yield %", min_value=0.0, value=0.0, step=0.05, format="%0.2f", key="q")

    st.write("Transaction costs $")

    k = st.number_input("Round trip transaction cost %", min_value=0.0, value=0.0, step=0.05, format="%0.2f", key="k", help="All expenses for buying and selling the option as a percentage")
    dt = st.number_input("Δ Time (trading days)", min_value=0.0, value=0.0, step=1.0, format="%0.2f", key="tc", help="The time between hedging adjustment's (days)")

    st.divider()

    st.subheader("Surface Plot Ranges")
    strike_min = st.number_input('Min Strike Price', min_value=1.0, value=S*0.8, step=0.1, key="strike_min")
    strike_max = st.number_input('Max Strike Price', min_value=1.0, value=S*1.2, step=0.1, key="strike_max")
    maturity_min = st.slider('Min Time to Maturity', min_value=0.1, max_value=2.0, value=0.1, step=0.1, key="maturity_min")
    maturity_max = st.slider('Max Time to Maturity', min_value=0.1, max_value=2.0, value=2.0, step=0.1, key="maturity_max")



tab1, tab2, tab3, tab4 = st.tabs(["Black-Scholes Model", "Leland's Model", "Option Surface Picker", "Implied Volatility"])

# --- STANDARD BLACK-SCHOLES PLOTS ---
with tab1:
    st.header("Black-Scholes Model Pricing")
    call_price, put_price = get_bsm_prices(T, K, S, v, r, q)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Call Option Value", f"${call_price:.2f}")
        bsm_call_args = ("Call", strike_min, strike_max, maturity_min, maturity_max, S, v, r, q)
        display_option_surface("Call Option Surface", generate_bsm_surface, bsm_call_args, "call", default_rotation=330)

    with col2:
        st.metric("Put Option Value", f"${put_price:.2f}")
        bsm_put_args = ("Put", strike_min, strike_max, maturity_min, maturity_max, S, v, r, q)
        display_option_surface("Put Option Surface", generate_bsm_surface, bsm_put_args, "put", default_rotation=230)

# --- LELAND'S MODEL PLOTS ---
with tab2:
    st.header("Leland's Model with Transaction Costs and Dividend Yield")

    if dt > 0:
        cash_call_price, cash_put_price, stock_call_price, stock_put_price = get_leland_prices(T, K, S, v, r, q, k, dt)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Call Options")

            st.metric("Cash-Adjusted Call Value", f"${cash_call_price:.2f}")
            leland_cash_call_args = ("Cash Call", strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt)
            display_option_surface("Cash Call Surface", generate_leland_surface, leland_cash_call_args, "leland_cash_call", default_rotation=330)

            st.metric("Stock-Adjusted Call Value", f"${stock_call_price:.2f}")
            leland_stock_call_args = ("Stock Call", strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt)
            display_option_surface("Stock Call Surface", generate_leland_surface, leland_stock_call_args, "leland_stock_call", default_rotation=330)

        with col2:
            st.subheader("Put Options")

            st.metric("Cash-Adjusted Put Value", f"${cash_put_price:.2f}")
            leland_cash_put_args = ("Cash Put", strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt)
            display_option_surface("Cash Put Surface", generate_leland_surface, leland_cash_put_args, "leland_cash_put", default_rotation=230)

            st.metric("Stock-Adjusted Put Value", f"${stock_put_price:.2f}")
            leland_stock_put_args = ("Stock Put", strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt)
            display_option_surface("Stock Put Surface", generate_leland_surface, leland_stock_put_args, "leland_stock_put", default_rotation=230)
    else:
        st.info("Enter a Δ Time (in the sidebar) greater than zero to display Leland's Model results.")

# --- OPTION SURFACE PICKER ---
with tab3:
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.header("Pick your Option Surface")

        bsm_model = st.selectbox(
            "Select Model for Option Surface",
            ["Black-Scholes", "Leland's Model"], 
            index=0)
        
        if bsm_model == "Black-Scholes":
            option_surface_type = st.selectbox(
            "Select Option Surface Type",
            ["Call", "Put"],
            index=0,
            )

        elif bsm_model == "Leland's Model":
            option_surface_type = st.selectbox(
            "Select Option Surface Type",
            ["Cash Call", "Stock Call", "Cash Put", "Stock Put"],
            index=0,
            )

        st.write("Adjust Plot View")

        default_rotation = 330 if "Call" in option_surface_type else 230
        elevation_val = st.slider('Elevation', 0, 90, 20, 5, key="e_picker")
        rotation_val = st.slider('Rotation', 0, 360, value=default_rotation, step=5, key="r_picker")
        

    with col2:
    
        if option_surface_type == "Put":
            bsm_put_args = ("Put", strike_min, strike_max, maturity_min, maturity_max, S, v, r, q)
            display_option_surface("Put Option Surface", generate_bsm_surface, bsm_put_args, "put2", default_rotation=0, elevation=elevation_val, rotation=rotation_val)
        elif option_surface_type == "Call":
            bsm_call_args = ("Call", strike_min, strike_max, maturity_min, maturity_max, S, v, r, q)
            display_option_surface("Call Option Surface", generate_bsm_surface, bsm_call_args, "call2", default_rotation=0, elevation=elevation_val, rotation=rotation_val)

        elif option_surface_type == "Cash Call":
            leland_cash_call_args = ("Cash Call", strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt)
            display_option_surface("Cash Call Surface", generate_leland_surface, leland_cash_call_args, "leland_cash_call", default_rotation=0, elevation=elevation_val, rotation=rotation_val)

        elif option_surface_type == "Stock Call":
            leland_stock_call_args = ("Stock Call", strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt)
            display_option_surface("Stock Call Surface", generate_leland_surface, leland_stock_call_args, "leland_stock_call", default_rotation=0, elevation=elevation_val, rotation=rotation_val)

        elif option_surface_type == "Cash Put":
            leland_cash_put_args = ("Cash Put", strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt)
            display_option_surface("Cash Put Surface", generate_leland_surface, leland_cash_put_args, "leland_cash_put", default_rotation=0, elevation=elevation_val, rotation=rotation_val)

        elif option_surface_type == "Stock Put":
            leland_stock_put_args = ("Stock Put", strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt)
            display_option_surface("Stock Put Surface", generate_leland_surface, leland_stock_put_args, "leland_stock_put", default_rotation=0, elevation=elevation_val, rotation=rotation_val)
    
# --- IMPLIED VOLATILITY CALCULATION ---
with tab4:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.header("Implied Volatility Calculation")
        st.write("Calculate the implied volatility of an option given its market price.")

        option_type = st.selectbox(
            "Select Option Type for Implied Volatility Calculation",
            ["call", "put"],
            index=0,
            )

        option_type_market_price = st.number_input(
                "Market Price of the Option $",
                min_value=0.0,
                value=call_price
            )

        option_type, implied_vol = get_implied_volatility(T, K, S, v, r, q, option_type, option_type_market_price)

        st.info(f"Implied Volatility for {option_type} Option: {implied_vol:.2f}")