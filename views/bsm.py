import streamlit as st
import sys
sys.path.append('views')

from bsm_model import BlackScholes
from plot_option import PlotOption
from bsm_leland_model import BlackScholesLeland

st.set_page_config(
    page_title="Black-Scholes Model",
    page_icon=":material/functions:",
    layout="wide",  # wide or centered
    initial_sidebar_state="expanded"

)

st.header("Original Black-Scholes Model Options Pricing")

st.markdown("""
        - [Jump to Original Black-Scholes Model](#original-black-scholes-model-options-pricing)
        - [Jump to Implied Volatility](#implied-volatility-calculation)
        - [Jump to Leland's Model](#leland-s-model-with-transaction-costs-and-dividend-yield)
        """)


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

    strike_min = st.number_input('Min Strike Price', min_value=1.0, value=S*0.8, step=0.1, key="strike_min")
    strike_max = st.number_input('Max Strike Price', min_value=1.0, value=S*1.2, step=0.1, key="strike_max")
    maturity_min = st.slider('Min Time to Maturity', min_value=0.1, max_value=2.0, value=0.1, step=0.1, key="maturity_min")
    maturity_max = st.slider('Max Time to Maturity', min_value=0.1, max_value=2.0, value=2.0, step=0.1, key="maturity_max")

st.divider()

bs_model = BlackScholes(T, K, S, v, r, q)
bsml_model = BlackScholesLeland(T,K,S,v,r,q,k,dt)
call_price, put_price = bs_model.calculate_prices()
vega = bs_model.vega()
if dt > 0:
    cash_call_price, cash_put_price, stock_call_price, stock_put_price = bsml_model.calculate_prices()

optionSurfacePlot = PlotOption(strike_min, strike_max, maturity_min, maturity_max, S, v, r, q)

col1, col2 = st.columns(2)

with col1:
    st.metric("CALL Value", f"${call_price:.2f}")
    st.divider()
    st.subheader("Call Option Surface")
    optionSurfacePlot.plot_option_surface("call")

with col2:
    st.metric("PUT Value", f"${put_price:.2f}")
    st.divider()
    st.subheader("Put Option Surface")
    optionSurfacePlot.plot_option_surface("put")

st.divider()

st.header("Leland's Model with Transaction Costs and Dividend Yield")

st.write("Leland's model incorporates transaction costs and dividend yield into the Black-Scholes framework.")


if dt > 0 and cash_call_price  > 0: # if one is > 0 then they all are :)

    st.metric("Cash Call Value", f"${cash_call_price:.2f}")

    st.metric("Stock Call Value", f"${stock_call_price:.2f}")

    st.metric("Cash Put Value", f"${cash_put_price:.2f}")

    st.metric("Stock Put Value", f"${stock_put_price:.2f}")

else:

    st.write("input a Δ Time")

st.divider()

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
)

option_type, implied_vol = bs_model.implied_volatility(option_type, option_type_market_price)

st.write(f"Implied Volatility for {option_type} Option: {implied_vol:.2f}")