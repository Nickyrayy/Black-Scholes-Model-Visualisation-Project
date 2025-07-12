import streamlit as st
import sys
sys.path.append('views')

from bsm_model import BlackScholes

st.set_page_config(
    page_title="Black-Scholes Model",
    page_icon=":material/functions:",
    layout="wide",  # wide or centered
    initial_sidebar_state="expanded"

)

st.write("BSM")

with st.sidebar:
    st.subheader("Required Variables")

    S = st.number_input(
        "Current Asset Price $", 
        min_value=0.0, 
        value=100.0, 
        step=5.0, 
        format="%0.2f",
        key="S",
    )

    K = st.number_input(
        "Current strike Price $", 
        min_value=0.0, 
        value=100.0, 
        step=5.0, 
        format="%0.2f",
        key="K",
    )

    T = st.number_input(
        "Time to expiration (Annualised)", 
        min_value=0.0, 
        value=1.0, 
        step=0.1, 
        format="%0.2f",
        key="T",
    )

    r = st.number_input(
        "Risk-Free Interest Rate % (Annualised)", 
        min_value=0.0, 
        value=5.0, 
        step=0.05, 
        format="%0.2f",
        key="r",
    )

    v= st.number_input(
        "Volatility %", 
        min_value=0.00, 
        value=20.0, 
        step=0.01, 
        format="%0.2f",
        key="v",
    )
        
    st.divider()

    st.subheader("Optional Variables")

    q = st.number_input(
        "Expected Dividend Yield %", 
        min_value=0.0, 
        value=0.0, 
        step=0.05, 
        format="%0.2f",
        key="q",
    )

    st.write("Transaction costs $")

    k = st.number_input(
        "Round trip transaction cost %",
        min_value=0.0,
        value=0.0,
        step=0.05,
        format="%0.2f",
        key="k",
        help="All expenses for buying and selling the option as a percentage"
    )

    dt = st.number_input(
    "Δ Time (trading days)", 
    min_value=0.0, 
    value=0.0, 
    step=1.0, 
    format="%0.2f",
    key="tc",
    help="The time between hedging adjustment's (days)",
    )

st.divider()

bs_model = BlackScholes(T, K, S, v, r, q)
call_price, put_price = bs_model.calculate_prices()
vega = bs_model.vega()

col1, col2 = st.columns(2)

with col1:
    st.metric("CALL Value", f"${call_price:.2f}")

with col2:
    st.metric("PUT Value", f"${put_price:.2f}")

option_type = st.selectbox(
"Select Option Type for Implied Volatility Calculation",
["call", "put"],
index=0,
)

option_type_market_price = st.number_input(
    "Market Price of the Option $",
    min_value=0.0,
)

option_type, implied_vol = bs_model.implied_volatility(option_type, option_type_market_price)

st.write(f"Implied Volatility for {option_type} Option: {implied_vol:.2f}")