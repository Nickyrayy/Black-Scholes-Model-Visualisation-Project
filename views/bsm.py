import streamlit as st
import sys

#from models.bsm_leland_model import BlackScholesLeland
sys.path.append('views')

from functions.computations import (
    get_bsm_prices,
    get_leland_prices,
    get_implied_volatility
)

from functions.helper import (
    generate_bsm_option_surface,
    generate_leland_option_surface,
    generate_bsm_vs_leland_option_surface
)

st.set_page_config(
    page_title="Black-Scholes Model",
    page_icon=":material/functions:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.title("Model Parameters")

    with st.container(border=True):
        st.subheader("Required Inputs")
        
        S = st.number_input("Current Asset Price $", min_value=0.0, value=100.0, step=5.0, format="%0.2f", key="S")
        K = st.number_input("Current strike Price $", min_value=0.0, value=100.0, step=5.0, format="%0.2f", key="K")
        T = st.number_input("Time to expiration (Annualised)", min_value=0.0, value=1.0, step=0.1, format="%0.2f", key="T")
        r = st.number_input("Risk-Free Interest Rate % (Annualised)", min_value=0.0, value=5.0, step=0.05, format="%0.2f", key="r")
        v = st.number_input("Volatility %", min_value=0.00, value=20.0, step=0.01, format="%0.2f", key="v")
    
    #st.divider()

    with st.container(border=True):

        st.subheader("Optional Inputs")

        q = st.number_input("Expected Dividend Yield %", min_value=0.0, value=0.0, step=0.05, format="%0.2f", key="q")
        st.write("Transaction costs $")
        k = st.number_input("Round trip transaction cost %", min_value=0.0, value=0.0, step=0.05, format="%0.2f", key="k", help="All expenses for buying and selling the option as a percentage")
        dt = st.number_input("δ Time (trading days)", min_value=0.0, value=0.0, step=1.0, format="%0.2f", key="tc", help="The time between hedging adjustment's (days)")

    #st.divider()

    with st.container(border=True):
        st.subheader("Surface Plot Ranges")
        strike_min = st.number_input('Min Strike Price', min_value=1.0, value=S*0.8, step=0.1, key="strike_min")
        strike_max = st.number_input('Max Strike Price', min_value=1.0, value=S*1.2, step=0.1, key="strike_max")
        maturity_min = st.slider('Min Time to Maturity', min_value=0.1, max_value=2.0, value=0.1, step=0.1, key="maturity_min")
        maturity_max = st.slider('Max Time to Maturity', min_value=0.1, max_value=2.0, value=2.0, step=0.1, key="maturity_max")


# --- TABS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Black-Scholes Model", "Leland's Model","BSM Vs BSML", "Option Surface Picker", "Implied Volatility"])

# --- TAB 1: STANDARD BLACK-SCHOLES PLOTS ---
with tab1:
    st.header("Black-Scholes Model Pricing")
    call_price, put_price = get_bsm_prices(T, K, S, v, r, q)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Call Option Value", f"${call_price:.2f}")
        generate_bsm_option_surface("Call", strike_min, strike_max, maturity_min, maturity_max, S, v, r, q)
    with col2:
        st.metric("Put Option Value", f"${put_price:.2f}")
        generate_bsm_option_surface("Put", strike_min, strike_max, maturity_min, maturity_max, S, v, r, q)

# --- TAB 2: LELAND'S MODEL PLOTS ---
with tab2:
    st.header("Leland's Model with Transaction Costs and Dividend Yield")

    if dt > 0:
        
        l_call_price, l_put_price = get_leland_prices(T, K, S, v, r, q, k, dt)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Transaction-Cost-Adjusted Call Value", f"${l_call_price:.2f}")
            generate_leland_option_surface("Call", strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt)

        with col2:
            st.metric("Transaction-Cost-Adjusted Put Value", f"${l_put_price:.2f}")
            generate_leland_option_surface("Put", strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt)

    else:
        st.info("Enter a Δ Time (in the sidebar) greater than zero to display Leland's Model results.")

# --- Tab 3: BSM vs Leland's Model Option Surface ---
with tab3:
    st.header("Black-Scholes vs Leland's Model Option Surface")

    if dt > 0:
        
        Le_call_price, Le_put_price = get_leland_prices(T, K, S, v, r, q, k, dt)
        bs_Call_price, bs_Put_price = get_bsm_prices(T, K, S, v, r, q)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Black-Scholes Call Value", f"${bs_Call_price:.2f}")
            st.metric("Leland's Call Value", f"${Le_call_price:.2f}")
            generate_bsm_vs_leland_option_surface("Call", strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt)

        with col2:
            st.metric("Black-Scholes Put Value", f"${bs_Put_price:.2f}")
            st.metric("Leland's Put Value", f"${Le_put_price:.2f}")
            generate_bsm_vs_leland_option_surface("Put", strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt)

    else:
        st.info("Enter a Δ Time (in the sidebar) greater than zero to display Leland's Model results.")


# --- TAB 4: OPTION SURFACE PICKER ---
with tab4:
    col1, col2, col3 = st.columns([1, 1.5, 0.5])

    with col1:
        st.header("Pick your Option Surface")

        with st.container(border=True):

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
            else: # Leland's Model
                option_surface_type = st.selectbox(
                "Select Option Surface Type",
                ["Call", "Put"],
                index=0,
                )

            st.write("Adjust Plot View")
            default_rotation = 330 if "Call" in option_surface_type else 230
            elevation_val = st.slider('Elevation', 0, 90, 20, 5, key="e_picker")
            rotation_val = st.slider('Rotation', 0, 360, value=default_rotation, step=5, key="r_picker")

    with col2:
        
        # Call the appropriate helper based on the selected model
        if bsm_model == "Black-Scholes":
            generate_bsm_option_surface(
                option_surface_type, 
                strike_min, strike_max, maturity_min, maturity_max, 
                S, v, r, q, 
                elevation=elevation_val, rotation=rotation_val
            )
        elif bsm_model == "Leland's Model":
            generate_leland_option_surface(
                option_surface_type, 
                strike_min, strike_max, maturity_min, maturity_max, 
                S, v, r, q, k, dt, 
                elevation=elevation_val, rotation=rotation_val
            )

# --- TAB 5: IMPLIED VOLATILITY CALCULATION ---
with tab5:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.header("Implied Volatility Calculation")
        st.write("Calculate the implied volatility of an option given its market price.")

        with st.container(border=True):
            option_type = st.selectbox(
                "Select Option Type for Implied Volatility Calculation",
                ["call", "put"],
                index=0,
                )
            
            # Set default market price based on selected option
            call_price, put_price = get_bsm_prices(T, K, S, v, r, q)
            default_market_price = call_price if option_type == 'call' else put_price

            option_type_market_price = st.number_input(
                    "Market Price of the Option $",
                    min_value=0.0,
                    value=default_market_price,
                    format="%.2f"
                )

        option_type, implied_vol = get_implied_volatility(T, K, S, v, r, q, option_type, option_type_market_price)

        with st.container(border=True):
            st.metric(f"Implied Volatility for {option_type.capitalize()} Option", f"{implied_vol:.2%}")
