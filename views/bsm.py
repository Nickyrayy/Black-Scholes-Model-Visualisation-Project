import streamlit as st
import sys
sys.path.append('views')

from models.bsm_model import BlackScholes
from graphPlots.plot_option_bsm import PlotOptionBSM
from graphPlots.plot_option_bsml import PlotOptionBSML
from models.bsm_leland_model import BlackScholesLeland

st.set_page_config(
    page_title="Black-Scholes Model",
    page_icon=":material/functions:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- HEADER ---
st.header("Original Black-Scholes Model Options Pricing")
st.markdown("""
- [Jump to Original Black-Scholes Model](#original-black-scholes-model-options-pricing)
- [Jump to Leland's Model](#leland-s-model-with-transaction-costs-and-dividend-yield)
- [Jump to Implied Volatility](#implied-volatility-calculation)
""")

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.subheader("Required Variables")
    S = st.number_input("Current Asset Price $", min_value=0.0, value=100.0, step=5.0, format="%0.2f", key="S")
    K = st.number_input("Current strike Price $", min_value=0.0, value=100.0, step=5.0, format="%0.2f", key="K")
    T = st.number_input("Time to expiration (Annualised)", min_value=0.0, value=1.0, step=0.1, format="%0.2f", key="T")
    r = st.number_input("Risk-Free Interest Rate % (Annualised)", min_value=0.0, value=5.0, step=0.05, format="%0.2f", key="r")
    v = st.number_input("Volatility %", min_value=0.00, value=20.0, step=0.01, format="%0.2f", key="v")
    
    st.divider()
    st.subheader("Optional Variables")
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

st.divider()

# --- MODEL AND PLOTTER INSTANTIATION ---
bs_model = BlackScholes(T, K, S, v, r, q)
call_price, put_price = bs_model.calculate_prices()

# Instantiate the plotters with all required parameters
regularOptionSurfacePlot = PlotOptionBSM(strike_min, strike_max, maturity_min, maturity_max, S, v, r, q)
lelandOptionSurfacePlot = PlotOptionBSML(strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt)

# --- STANDARD BLACK-SCHOLES PLOTS ---
col1, col2 = st.columns(2)
with col1:
    st.metric("CALL Value", f"${call_price:.2f}")
    st.divider()
    st.subheader("Call Option Surface")
    # Generate the figure and then plot it
    call_fig = regularOptionSurfacePlot.plot_option_surface("call")
    st.pyplot(call_fig)

with col2:
    st.metric("PUT Value", f"${put_price:.2f}")
    st.divider()
    st.subheader("Put Option Surface")
    # Generate the figure and then plot it
    put_fig = regularOptionSurfacePlot.plot_option_surface("put")
    st.pyplot(put_fig)

st.divider()

# --- LELAND'S MODEL PLOTS ---
st.header("Leland's Model with Transaction Costs and Dividend Yield")
st.write("Leland's model incorporates transaction costs and dividend yield into the Black-Scholes framework.")

# Calculate Leland prices only if needed
if dt > 0:
    bsml_model = BlackScholesLeland(T, K, S, v, r, q, k, dt)
    cash_call_price, cash_put_price, stock_call_price, stock_put_price = bsml_model.calculate_prices()

    col1_1, col1_2, col2_1, col2_2 = st.columns(4)

    with col1_1:
        st.metric("Cash CALL Value", f"${cash_call_price:.2f}")
        st.divider()
        st.subheader("Cash Call Option Surface")
        
        # The placeholder pattern to get sliders UNDER the plot
        plot_placeholder = st.empty()
        elevation = st.slider('Elevation', 0, 90, 20, 5, key="e_cash_call")
        rotation = st.slider('Rotation', 0, 360, 330, 5, key="r_cash_call")
        fig = lelandOptionSurfacePlot.plot_option_surface("cash_call", elevation, rotation)
        plot_placeholder.pyplot(fig)

    with col1_2:
        st.metric("Cash PUT Value", f"${cash_put_price:.2f}")
        st.divider()
        st.subheader("Cash Put Option Surface")
        
        plot_placeholder = st.empty()
        elevation = st.slider('Elevation', 0, 90, 20, 5, key="e_cash_put")
        rotation = st.slider('Rotation', 0, 360, 230, 5, key="r_cash_put")
        fig = lelandOptionSurfacePlot.plot_option_surface("cash_put", elevation, rotation)
        plot_placeholder.pyplot(fig)

    with col2_1:
        st.metric("Stock CALL Value", f"${stock_call_price:.2f}")
        st.divider()
        st.subheader("Stock Call Option Surface")
        
        plot_placeholder = st.empty()
        elevation = st.slider('Elevation', 0, 90, 20, 5, key="e_stock_call")
        rotation = st.slider('Rotation', 0, 360, 330, 5, key="r_stock_call")
        fig = lelandOptionSurfacePlot.plot_option_surface("stock_call", elevation, rotation)
        plot_placeholder.pyplot(fig)

    with col2_2:
        st.metric("Stock PUT Value", f"${stock_put_price:.2f}")
        st.divider()
        st.subheader("Stock Put Option Surface")
        
        plot_placeholder = st.empty()
        elevation = st.slider('Elevation', 0, 90, 20, 5, key="e_stock_put")
        rotation = st.slider('Rotation', 0, 360, 230, 5, key="r_stock_put")
        fig = lelandOptionSurfacePlot.plot_option_surface("stock_put", elevation, rotation)
        plot_placeholder.pyplot(fig)
else:
    st.info("Enter a Δ Time (in the sidebar) greater than zero to display Leland's Model results.")

st.divider()

# --- IMPLIED VOLATILITY ---
st.header("Implied Volatility Calculation")
st.write("Calculate the implied volatility of an option given its market price.")

iv_option_type = st.selectbox(
    "Select Option Type for Implied Volatility Calculation",
    ["call", "put"],
    index=0,
    key="iv_type"
)

market_price = st.number_input(
    "Market Price of the Option $",
    min_value=0.01,
    value=call_price, # Default to the calculated BSM price
    step=0.1
)

if st.button("Calculate Implied Volatility"):
    try:
        implied_vol = bs_model.implied_volatility(iv_option_type, market_price)
        st.success(f"Implied Volatility for {iv_option_type.capitalize()} Option: {implied_vol:.2%}")
    except ValueError as e:
        st.error(f"Could not calculate Implied Volatility: {e}")

