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
- [Jump to Implied Volatility And Pick Your Own Option Surface](#implied-volatility-calculation)
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

# --- STANDARD BLACK-SCHOLES PLOTS ---
call_price, put_price = get_bsm_prices(T, K, S, v, r, q)

col1, col2 = st.columns(2)
with col1:
    st.metric("CALL Value", f"${call_price:.2f}")
    st.divider()
    st.subheader("Call Option Surface")
    # Generate the figure and then plot it
    plot_placeholder = st.empty()
    st.divider()
    elevation = st.slider('Elevation', 0, 90, 20, 5, key="e_call")
    rotation = st.slider('Rotation', 0, 360, 330, 5, key="r_call")
    fig = generate_bsm_surface("Call", elevation, rotation, strike_min, strike_max, maturity_min, maturity_max, S, v, r, q)
    plot_placeholder.pyplot(fig)

with col2:
    st.metric("PUT Value", f"${put_price:.2f}")
    st.divider()
    st.subheader("Put Option Surface")
    # Generate the figure and then plot it
    plot_placeholder = st.empty()
    st.divider()
    elevation = st.slider('Elevation', 0, 90, 20, 5, key="e_put")
    rotation = st.slider('Rotation', 0, 360, 230, 5, key="r_put")
    fig = generate_bsm_surface("Put", elevation, rotation, strike_min, strike_max, maturity_min, maturity_max, S, v, r, q)
    plot_placeholder.pyplot(fig)

st.divider()

# --- LELAND'S MODEL PLOTS ---
st.header("Leland's Model with Transaction Costs and Dividend Yield")
st.write("Leland's model incorporates transaction costs and dividend yield into the Black-Scholes framework.")

# Calculate Leland prices only if needed
if dt > 0:
    cash_call_price, cash_put_price, stock_call_price, stock_put_price = get_leland_prices(T, K, S, v, r, q, k, dt)

    col1_1, col1_2, col2_1, col2_2 = st.columns(4)

    with col1_1:
        st.metric("Cash CALL Value", f"${cash_call_price:.2f}")
        st.divider()
        st.subheader("Cash Call Option Surface")
        
        # The placeholder pattern to get sliders UNDER the plot
        plot_placeholder = st.empty()
        elevation = st.slider('Elevation', 0, 90, 20, 5, key="e_cash_call")
        rotation = st.slider('Rotation', 0, 360, 330, 5, key="r_cash_call")
        fig = generate_leland_surface("Cash Call", elevation, rotation, strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt)
        plot_placeholder.pyplot(fig)

    with col1_2:
        st.metric("Stock CALL Value", f"${stock_call_price:.2f}")
        st.divider()
        st.subheader("Stock Call Option Surface")
        
        plot_placeholder = st.empty()
        elevation = st.slider('Elevation', 0, 90, 20, 5, key="e_stock_call")
        rotation = st.slider('Rotation', 0, 360, 330, 5, key="r_stock_call")
        fig = generate_leland_surface("Stock Call", elevation, rotation, strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt)
        plot_placeholder.pyplot(fig)

    with col2_1:
        st.metric("Cash PUT Value", f"${cash_put_price:.2f}")
        st.divider()
        st.subheader("Cash Put Option Surface")
        
        plot_placeholder = st.empty()
        elevation = st.slider('Elevation', 0, 90, 20, 5, key="e_cash_put")
        rotation = st.slider('Rotation', 0, 360, 230, 5, key="r_cash_put")
        fig = generate_leland_surface("Cash Put", elevation, rotation, strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt)
        plot_placeholder.pyplot(fig)


    with col2_2:
        st.metric("Stock PUT Value", f"${stock_put_price:.2f}")
        st.divider()
        st.subheader("Stock Put Option Surface")
        
        plot_placeholder = st.empty()
        elevation = st.slider('Elevation', 0, 90, 20, 5, key="e_stock_put")
        rotation = st.slider('Rotation', 0, 360, 230, 5, key="r_stock_put")
        fig = generate_leland_surface("Stock Put", elevation, rotation, strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt)
        plot_placeholder.pyplot(fig)
else:
    st.info("Enter a Δ Time (in the sidebar) greater than zero to display Leland's Model results.")

st.divider()

# --- IMPLIED VOLATILITY ---

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

    st.divider()
    st.header("Option Surface Parameters")
    st.write("Visualize the option surface for different parameters.")

    elevation = st.slider('Elevation', 0, 90, 20, 5, key="n_surface_bsm")
    rotation = st.slider('Rotation', 0, 360, 330, 5, key="u_surface_bsm")

with col2:
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
        
        plot_placeholder = st.empty()
        
        fig = generate_bsm_surface(option_surface_type, elevation, rotation, strike_min, strike_max, maturity_min, maturity_max, S, v, r, q)
        plot_placeholder.pyplot(fig)

    if bsm_model == "Leland's Model":
        option_surface_type = st.selectbox(
        "Select Option Surface Type",
        ["Cash Call", "Stock Call", "Cash Put", "Stock Put"],
        index=0,
        )
        plot_placeholder = st.empty()
        
        fig = generate_leland_surface(option_surface_type, elevation, rotation, strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt)
        plot_placeholder.pyplot(fig)

