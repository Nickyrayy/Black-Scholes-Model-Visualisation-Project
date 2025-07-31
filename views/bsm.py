import streamlit as st
import sys
sys.path.append('views')

from functions.computations import (
    get_bsm_prices,
    get_leland_prices,
    get_implied_volatility,
    get_theta,
    get_vega,
    get_gamma,
    get_delta,
    get_rho
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

# --- Sidebar Styling ---
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }
    </style>
""", unsafe_allow_html=True)


# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.title("Model Parameters")

    with st.container(border=True):
        st.subheader("Required Inputs")
        
        S = st.number_input("Current Asset Price $", min_value=0.0, value=120.0, step=5.0, format="%0.2f", key="S")
        K = st.number_input("Current strike Price $", min_value=0.0, value=100.0, step=5.0, format="%0.2f", key="K")
        T = st.number_input("Time to expiration (Annualised)", min_value=0.0, value=1.0, step=0.1, format="%0.2f", key="T")
        r = st.number_input("Risk-Free Interest Rate % (Annualised)", min_value=0.0, value=5.0, step=0.05, format="%0.2f", key="r")
        v = st.number_input("Volatility %", min_value=0.00, value=20.0, step=0.01, format="%0.2f", key="v")

    with st.container(border=True):

        st.subheader("Optional Inputs")

        q = st.number_input("Expected Dividend Yield %", min_value=0.0, value=0.0, step=0.05, format="%0.2f", key="q")
        st.write("Transaction costs $")
        k = st.number_input("Round trip transaction cost %", min_value=0.0, value=0.0, step=0.05, format="%0.2f", key="k", help="All expenses for buying and selling the option as a percentage")
        dt = st.number_input("Δ Time (trading days)", min_value=0.0, value=0.0, step=1.0, format="%0.2f", key="tc", help="The time between hedging adjustment's (days)")

    with st.container(border=True):
        st.subheader("Surface Plot Ranges")
        strike_min = st.number_input('Min Strike Price', min_value=1.0, value=S*0.8, step=0.1, key="strike_min")
        strike_max = st.number_input('Max Strike Price', min_value=1.0, value=S*1.2, step=0.1, key="strike_max")
        maturity_min = st.slider('Min Time to Maturity', min_value=0.1, max_value=2.0, value=0.1, step=0.1, key="maturity_min")
        maturity_max = st.slider('Max Time to Maturity', min_value=0.1, max_value=2.0, value=2.0, step=0.1, key="maturity_max")

# --- TABS ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Black-Scholes Model", "Leland's Model","BSM Vs BSML", "Option Surface Picker", "Implied Volatility & Greeks", "Implied Volatility & Greeks Picker"])

# --- TAB 1: STANDARD BLACK-SCHOLES PLOTS ---
with tab1:
    st.header("Black-Scholes Model Pricing")
    call_price, put_price = get_bsm_prices(T, K, S, v, r, q)
    call_price_on_expiry = max(S - K, 0)
    put_price_on_expiry = max(K - S, 0)

    col1, col2 = st.columns(2)
    with col1:
        st.header("Call Option Value")
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            st.metric("Value at Expiry", f"${call_price_on_expiry:.2f}")
        with col1_2:
            st.metric("Current Premium", f"${call_price - call_price_on_expiry:.2f}")
        generate_bsm_option_surface("Call", strike_min, strike_max, maturity_min, maturity_max, S, v, r, q)
    with col2:
        st.header("Put Option Value")
        col2_1, col2_2 = st.columns(2)
        with col2_1:
            st.metric("Value at Expiry", f"${put_price_on_expiry:.2f}")
        with col2_2:
            st.metric("Current Premium", f"${put_price - put_price_on_expiry:.2f}")
        generate_bsm_option_surface("Put", strike_min, strike_max, maturity_min, maturity_max, S, v, r, q)

# --- TAB 2: LELAND'S MODEL PLOTS ---
with tab2:
    st.header("Leland's Model with Transaction Costs and Dividend Yield")

    if dt > 0:
        l_call_price, l_put_price = get_leland_prices(T, K, S, v, r, q, k, dt)

        col1, col2 = st.columns(2)
        with col1:
            st.header("Call Option Value")
            col1_1, col1_2 = st.columns(2)
            with col1_1:
                st.metric("Value at Expiry", f"${call_price_on_expiry:.2f}")
            with col1_2:
                st.metric("Current Premium", f"${l_call_price - call_price_on_expiry:.2f}")
            generate_leland_option_surface("Call", strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt)

        with col2:
            st.header("Put Option Value")
            col2_1, col2_2 = st.columns(2)
            with col2_1:
                st.metric("Value at Expiry", f"${put_price_on_expiry:.2f}")
            with col2_2:
                st.metric("Current Premium", f"${l_put_price - put_price_on_expiry:.2f}")
            generate_leland_option_surface("Put", strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt)

    else:
        st.warning("Enter a Δ Time (in the sidebar) greater than zero to display Leland's Model results.")

# --- Tab 3: BSM vs Leland's Model Option Surface ---
with tab3:
    st.header("Black-Scholes vs Leland's Model Option Surface")

    st.divider()

    if dt > 0:
        
        Le_call_price, Le_put_price = get_leland_prices(T, K, S, v, r, q, k, dt)
        bs_Call_price, bs_Put_price = get_bsm_prices(T, K, S, v, r, q)

        col1_t, col2_t = st.columns(2)
        with col1_t:
            st.header("Call Value")
        with col2_t:
            st.header("Put Value")

        col1, col2, col3, col4 = st.columns(4, gap="small")

        with col1:
            st.subheader("Black-Scholes")

            col1_bsm_c, col2_bsm_c = st.columns(2)
            with col1_bsm_c:
                st.metric("Value at Expiry", f"${call_price_on_expiry:.2f}")
            with col2_bsm_c:
                st.metric("Current Premium", f"${call_price - call_price_on_expiry:.2f}")

        with col2:
            st.subheader("Leland's")

            col1_le_c, col2_le_c = st.columns(2)
            with col1_le_c:
                st.metric("Value at Expiry", f"${call_price_on_expiry:.2f}")
            with col2_le_c:
                st.metric("Current Premium", f"${l_call_price - call_price_on_expiry:.2f}")

        with col3:
            st.subheader("Black-Scholes")
            col1_bsm_p, col2_bsm_p = st.columns(2)
            with col1_bsm_p:
                st.metric("Value at Expiry", f"${put_price_on_expiry:.2f}")
            with col2_bsm_p:
                st.metric("Current Premium", f"${put_price - put_price_on_expiry:.2f}")
        
        with col4:
            st.subheader("Leland's")
            col1_le_p, col2_le_p = st.columns(2)
            with col1_le_p:
                st.metric("Value at Expiry", f"${put_price_on_expiry:.2f}")
            with col2_le_p:
                st.metric("Current Premium", f"${l_put_price - put_price_on_expiry:.2f}")

        col1_g, col2_g = st.columns(2)

        with col1_g:
            generate_bsm_vs_leland_option_surface("Call", strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt)

        with col2_g:
            generate_bsm_vs_leland_option_surface("Put", strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt)
    else:
        st.warning("Enter a Δ Time (in the sidebar) greater than zero to display Leland's Model results.")

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
            else: # leland's Model
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

# --- TAB 5: IMPLIED VOLATILITY AND GREEKS CALCULATION ---
with tab5:

    col1_tab5, col2_tab5, col3_tab5 = st.columns([3, 8, 3])

    with col2_tab5:
        st.header("Implied Volatility and Greeks Calculation")
        with st.container(border=True):
                st.subheader("Implied Volatility and Greeks Calculation")
                st.write("Calculate the Implied Volatility (given its market price) or one of the Greeks of an option.")



                impl_vol_or_greeks = st.selectbox(
                    "Select Calculation Type",
                    ["Implied Volatility", "Delta", "Theta", "Vega", "Gamma", "Rho"],
                    index=0,
                    key="impl_vol_or_greeks"
                )

                with st.expander("View Variables that impact **Implied Volatility** or **Greeks**"):
                    st.markdown(
                        """
                        - **$S$**: Current price of the underlying asset
                        - **$K$**: Strike price of the option
                        - **$T-t$**: Time to expiration (in years)
                        - **$r$**: Risk-free interest rate
                        - **$\\sigma$**: Volatility of the underlying asset's returns
                        - **$q$**: Dividend yield of the underlying asset
                        - **$k$**: Transaction costs (For Leland's model)
                        - **$dt$**: Time delta (For Leland's model)
                        """
                )

                model_type = st.selectbox(
                    f"Select Model for Implied Volatility or Greeks Calculation",
                    ["Black-Scholes", "Leland's Model"],
                    index=0,
                    key=f"Implied Volatility or greeks model_type"
                )

                if model_type == "Leland's Model":
                    if dt <= 0:
                        st.warning("Please enter a Δ Time (in the sidebar) greater than zero to use Leland's Model.")
                        st.stop()
                    call_price, put_price = get_leland_prices(T, K, S, v, r, q, k, dt)
                else:
                    call_price, put_price = get_bsm_prices(T, K, S, v, r, q)
                    
                option_type = st.selectbox(
                    f"Select Option Type for Implied Volatility Calculation",
                    ["Call", "Put"],
                    index=0,
                    key=f"Implied Volatility or greeks option_type"
                    )
                
                if impl_vol_or_greeks == "Implied Volatility":
                    option_type_market_price = st.number_input(
                            "Market Price of the Option $",
                            min_value=0.0,
                            value=float(call_price_on_expiry * 1.5 if option_type == "Call" else put_price_on_expiry * 1.5),
                            format="%.2f",
                            step= 0.01,
                            key=f"Implied Volatility or greeks market_price"
                        )
                    option_type_market_price = float(option_type_market_price)
                else:
                    option_type_market_price = None


                if option_type == "Call":
                    option_price = call_price
                else:
                    option_price = put_price

                if impl_vol_or_greeks == "Implied Volatility":
                    greek_output = get_implied_volatility(T, K, S, v, r, q, k, dt, option_type, option_type_market_price, model_type)
                    
                elif impl_vol_or_greeks == "Delta":
                    call_greek_output, put_greek_output = get_delta(T, K, S, v, r, q, k, dt, model_type)

                    if option_type == "Call":
                        greek_output = call_greek_output
                    else:
                        greek_output = put_greek_output

                elif impl_vol_or_greeks == "Theta":
                    call_greek_output, put_greek_output = get_theta(T, K, S, v, r, q, k, dt, model_type)

                    if option_type == "Call":
                        call_greek_output /= 100
                        greek_output = call_greek_output
                    else:
                        put_greek_output /= 100
                        greek_output = put_greek_output

                elif impl_vol_or_greeks == "Vega":
                    greek_output = get_vega(T, K, S, v, r, q, k, dt, model_type)
                    greek_output /= 100

                elif impl_vol_or_greeks == "Gamma":
                    greek_output = get_gamma(T, K, S, v, r, q, k, dt, model_type)

                elif impl_vol_or_greeks == "Rho":
                    call_greek_output, put_greek_output = get_rho(T, K, S, v, r, q, k, dt, model_type)

                    if option_type == "Call":
                        call_greek_output /= 100
                        greek_output = call_greek_output
                    else:
                        put_greek_output /= 100
                        greek_output = put_greek_output

                with st.container(border=True):
                    col1_1, col2_1 = st.columns(2)
                    with col1_1:
                        st.metric(f"{option_type} Option Model Price", f"${option_price:.2f}")
                    with col2_1:
                        st.metric(f"Implied Volatility for {option_type}", f"{greek_output:.3f}")

# --- TAB 6: IMPLIED VOLATILITY AND GREEKS PICKER CALCULATION ---
with tab6:
    col1_page, col2_page, col3_page = st.columns([1, 1, 1])

    with col1_page:
        st.header("Put & Call")

        with st.container(border=True):
            st.subheader("Implied Volatility Calculation")
            st.write("Calculate the Implied Volatility of an option given its market price.")
            with st.expander("View Variables that impact **Implied Volatility**"):
                st.markdown(
                    """
                    - **$S$**: Current price of the underlying asset
                    - **$K$**: Strike price of the option
                    - **$T-t$**: Time to expiration (in years)
                    - **$r$**: Risk-free interest rate
                    - **$\\sigma$**: Volatility of the underlying asset's returns
                    - **$q$**: Dividend yield of the underlying asset
                    - **$k$**: Transaction costs (For Leland's model)
                    - **$dt$**: Time delta (For Leland's model)
                    """
            )

            model_type = st.selectbox(
                f"Select Model for Implied Volatility Calculation",
                ["Black-Scholes", "Leland's Model"],
                index=0,
                key=f"Implied Volatility_model_type"
            )

            if model_type == "Leland's Model":
                if dt <= 0:
                    st.warning("Please enter a Δ Time (in the sidebar) greater than zero to use Leland's Model.")
                    st.stop()
                call_price, put_price = get_leland_prices(T, K, S, v, r, q, k, dt)
            else:
                call_price, put_price = get_bsm_prices(T, K, S, v, r, q)
                
            option_type = st.selectbox(
                f"Select Option Type for Implied Volatility Calculation",
                ["Call", "Put"],
                index=0,
                key=f"Implied Volatility_option_type"
                )
            
            option_type_market_price = st.number_input(
                    "Market Price of the Option $",
                    min_value=0.0,
                    value=float(call_price_on_expiry * 1.5 if option_type == "Call" else put_price_on_expiry * 1.5),
                    format="%.2f",
                    step= 0.01,
                    key=f"Implied Volatility_market_price"
                )

            option_type_market_price = float(option_type_market_price) # fix for whole numbers not being handled right

            if option_type == "Call":
                option_price = call_price
            else:
                option_price = put_price

            greek_output = get_implied_volatility(T, K, S, v, r, q, k, dt, option_type, option_type_market_price, model_type)

            with st.container(border=True):
                col1_1, col2_1 = st.columns(2)
                with col1_1:
                    st.metric(f"{option_type} Option Model Price", f"${option_price:.2f}")
                with col2_1:
                    st.metric(f"Implied Volatility for {option_type}", f"{greek_output:.3f}")

        with st.container(border=True):
            st.subheader("Vega Calculation")
            st.write("Calculate the Vega of an option given its market price.")
            with st.expander("View Variables that impact **Vega** the most"):
                st.markdown(
                    """
                    - **$T-t$**: Time to expiry is the most important factor for Vega. As time to expiry increases, Vega increases.
                    - **$K$**: The strike price of the option. Vega is highest when the option is at-the-money.
                    - **$\\sigma$**: Volatility of the underlying asset's returns. Higher volatility increases Vega.
                    """
            )

            greek_model = "vega"
        
            model_type = st.selectbox(
                f"Select Model for {greek_model} Calculation",
                ["Black-Scholes", "Leland's Model"],
                index=0,
                key=f"{greek_model}_model_type"
            )

            if model_type == "Leland's Model":
                if dt <= 0:
                    st.warning("Please enter a Δ Time (in the sidebar) greater than zero to use Leland's Model.")
                    st.stop()
                call_price, put_price = get_leland_prices(T, K, S, v, r, q, k, dt)
            else:
                call_price, put_price = get_bsm_prices(T, K, S, v, r, q)
                
            option_type = st.selectbox(
                f"Select Option Type for {greek_model} Calculation",
                ["Call", "Put"],
                index=0,
                key=f"{greek_model}_option_type"
            )

            if option_type == "Call":
                option_price = call_price
            else:
                option_price = put_price

            greek_output = get_vega(T, K, S, v, r, q, k, dt, model_type)
            greek_output /= 100 # Vega is often expressed per 1% change in volatility, so we divide by 100

            with st.container(border=True):
                col1_2, col2_2 = st.columns(2)
                with col1_2:
                    st.metric(f"{option_type} Option Model Price", f"${option_price:.2f}")
                with col2_2:
                    st.metric(f"{greek_model} for {option_type}", f"{greek_output:.3f}")

        with st.container(border=True):
            st.subheader("Gamma Calculation")
            st.write("Calculate the Gamma of an option given its market price.")
            with st.expander("View Variables that impact **Gamma** the most"):
                st.markdown(
                    """
                    - **$T-t$**: Time to expiry is the most important factor for Gamma. As time to expiry decreases, Gamma increases.
                    - **$K$**: The strike price of the option. Gamma is highest when the option is at-the-money.
                    """
            )

            greek_model = "Gamma"
        
            model_type = st.selectbox(
                f"Select Model for {greek_model} Calculation",
                ["Black-Scholes", "Leland's Model"],
                index=0,
                key=f"{greek_model}_model_type"
            )

            if model_type == "Leland's Model":
                if dt <= 0:
                    st.warning("Please enter a Δ Time (in the sidebar) greater than zero to use Leland's Model.")
                    st.stop()
                call_price, put_price = get_leland_prices(T, K, S, v, r, q, k, dt)
            else:
                call_price, put_price = get_bsm_prices(T, K, S, v, r, q)
                
            option_type = st.selectbox(
                f"Select Option Type for {greek_model} Calculation",
                ["Call", "Put"],
                index=0,
                key=f"{greek_model}_option_type"
            )

            if option_type == "Call":
                option_price = call_price
            else:
                option_price = put_price

            greek_output = get_gamma(T, K, S, v, r, q, k, dt, model_type)

            with st.container(border=True):
                col1_3, col2_3 = st.columns(2)
                with col1_3:
                    st.metric(f"{option_type} Option Model Price", f"${option_price:.2f}")
                with col2_3:
                    st.metric(f"{greek_model} for {option_type}", f"{greek_output:.3f}")

    with col2_page:
        st.header("Call")

        with st.container(border=True):
            st.subheader("Call Delta Calculation")
            st.write("Calculate the Delta of an option given its market price.")
            with st.expander("View Variables that impact **Delta**"):
                st.markdown(
                    """
                    - **$$$**: Money-ness of the option.
                        - **In-the-money**: Strike price below the current stock price.
                        - **At-the-money**: Strike price equal to the current stock price.
                        - **Out-of-the-money**: Strike price above the current stock price.
                    - **$T-t$**: Time to expiration (in years)
                    - **$\\sigma$**: Volatility of the underlying asset's returns
                    """
            )

            greek_model = "Delta"
            option_type = "Call"
        
            model_type = st.selectbox(
                f"Select Model for {greek_model} Calculation",
                ["Black-Scholes", "Leland's Model"],
                index=0,
                key=f"{greek_model}_call"
            )

            if model_type == "Leland's Model":
                if dt <= 0:
                    st.warning("Please enter a Δ Time (in the sidebar) greater than zero to use Leland's Model.")
                    st.stop()
                call_price, put_price = get_leland_prices(T, K, S, v, r, q, k, dt)
            else:
                call_price, put_price = get_bsm_prices(T, K, S, v, r, q)

            Call_Delta, Put_Delta = get_delta(T, K, S, v, r, q, k, dt, model_type)

            with st.container(border=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(f"{option_type} Option Model Price", f"${call_price:.2f}")
                with col2:
                    st.metric(f"{greek_model} for {option_type}", f"{Call_Delta:.3f}")

        with st.container(border=True):
            st.subheader("Call Theta Calculation")
            st.write("Calculate the Theta of a call option given its market price.")
            with st.expander("View Variables that impact **Theta**"):
                st.markdown(
                    """
                    - **$T-t$**: Time to expiration (in years)
                    - **$K$**: Strike price of the option
                    - **$\\sigma$**: Volatility of the underlying asset's returns
                    - **$r$**: Risk-free interest rate
                    - **$q$**: Dividend yield of the underlying asset
                    - **$k$**: Transaction costs (For Leland's model)
                    - **$dt$**: Time delta (For Leland's model)
                    """
                )

            greek_model = "Theta"
            option_type = "Call"
        
            model_type = st.selectbox(
                f"Select Model for {greek_model} Calculation",
                ["Black-Scholes", "Leland's Model"],
                index=0,
                key=f"{greek_model}_call_theta"
            )

            if model_type == "Leland's Model":
                if dt <= 0:
                    st.warning("Please enter a Δ Time (in the sidebar) greater than zero to use Leland's Model.")
                    st.stop()
                call_price, put_price = get_leland_prices(T, K, S, v, r, q, k, dt)
            else:
                call_price, put_price = get_bsm_prices(T, K, S, v, r, q)

            theta_call, theta_put = get_theta(T, K, S, v, r, q, k, dt, model_type)
            # theta is often expressed per day, so we divide by 365
            theta_call /= 365

            with st.container(border=True):
                col1_2, col2_2 = st.columns(2)
                with col1_2:
                    st.metric(f"{option_type} Option Model Price", f"${call_price:.2f}")
                with col2_2:
                    st.metric(f"{greek_model} for {option_type}", f"{theta_call:.3f}")
        
        with st.container(border=True):
            st.subheader("Call Rho Calculation")
            st.write("Calculate the Rho of a call option given its market price.")
            with st.expander("View Variables that impact **Rho**"):
                st.markdown(
                    """
                    - **$T-t$**: Time to expiration (in years)
                    - **$K$**: Strike price of the option
                    - **$\\sigma$**: Volatility of the underlying asset's returns
                    - **$r$**: Risk-free interest rate
                    - **$q$**: Dividend yield of the underlying asset
                    - **$k$**: Transaction costs (For Leland's model)
                    - **$dt$**: Time delta (For Leland's model)
                    """
                )

            greek_model = "Rho"
            option_type = "Call"
        
            model_type = st.selectbox(
                f"Select Model for {greek_model} Calculation",
                ["Black-Scholes", "Leland's Model"],
                index=0,
                key=f"{greek_model}_call_rho"
            )

            if model_type == "Leland's Model":
                if dt <= 0:
                    st.warning("Please enter a Δ Time (in the sidebar) greater than zero to use Leland's Model.")
                    st.stop()
                call_price, put_price = get_leland_prices(T, K, S, v, r, q, k, dt)
            else:
                call_price, put_price = get_bsm_prices(T, K, S, v, r, q)

            rho_call, rho_put = get_rho(T, K, S, v, r, q, k, dt, model_type)
            # rho is often expressed per 1% change in interest rates, so we divide by 100
            rho_call /= 100

            with st.container(border=True):
                col1_2, col2_2 = st.columns(2)
                with col1_2:
                    st.metric(f"{option_type} Option Model Price", f"${call_price:.2f}")
                with col2_2:
                    st.metric(f"{greek_model} for {option_type}", f"{rho_call:.3f}")
                    
    with col3_page:
        st.header("Put")

        with st.container(border=True):
            st.subheader("Put Delta Calculation")
            st.write("Calculate the Delta of a put option given its market price.")
            with st.expander("View Variables that impact **Delta**"):
                st.markdown(
                    """
                    - **$$$**: Money-ness of the option.
                        - **In-the-money**: Strike price above the current stock price.
                        - **At-the-money**: Strike price equal to the current stock price.
                        - **Out-of-the-money**: Strike price below the current stock price.
                    - **$T-t$**: Time to expiration (in years)
                    - **$\\sigma$**: Volatility of the underlying asset's returns
                    """
            )

            greek_model = "Delta"
            option_type = "Put"
        
            model_type = st.selectbox(
                f"Select Model for {greek_model} Calculation",
                ["Black-Scholes", "Leland's Model"],
                index=0,
                key=f"{greek_model}_put"
            )

            if model_type == "Leland's Model":
                if dt <= 0:
                    st.warning("Please enter a Δ Time (in the sidebar) greater than zero to use Leland's Model.")
                    st.stop()
                call_price, put_price = get_leland_prices(T, K, S, v, r, q, k, dt)
            else:
                call_price, put_price = get_bsm_prices(T, K, S, v, r, q)

            Call_Delta, Put_Delta = get_delta(T, K, S, v, r, q, k, dt, model_type)

            with st.container(border=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(f"{option_type} Option Model Price", f"${put_price:.2f}")
                with col2:
                    st.metric(f"{greek_model} for {option_type}", f"{Put_Delta:.3f}")
        
        with st.container(border=True):
            st.subheader("Put Theta Calculation")
            st.write("Calculate the Theta of a put option given its market price.")
            with st.expander("View Variables that impact **Theta**"):
                st.markdown(
                    """
                    - **$T-t$**: Time to expiration (in years)
                    - **$K$**: Strike price of the option
                    - **$\\sigma$**: Volatility of the underlying asset's returns
                    - **$r$**: Risk-free interest rate
                    - **$q$**: Dividend yield of the underlying asset
                    - **$k$**: Transaction costs (For Leland's model)
                    - **$dt$**: Time delta (For Leland's model)
                    """
                )

            greek_model = "Theta"
            option_type = "Put"
        
            model_type = st.selectbox(
                f"Select Model for {greek_model} Calculation",
                ["Black-Scholes", "Leland's Model"],
                index=0,
                key=f"{greek_model}_put_theta"
            )

            if model_type == "Leland's Model":
                if dt <= 0:
                    st.warning("Please enter a Δ Time (in the sidebar) greater than zero to use Leland's Model.")
                    st.stop()
                call_price, put_price = get_leland_prices(T, K, S, v, r, q, k, dt)
            else:
                call_price, put_price = get_bsm_prices(T, K, S, v, r, q)

            theta_call, theta_put = get_theta(T, K, S, v, r, q, k, dt, model_type)
            # theta is often expressed per day, so we divide by 365
            theta_put /= 365

            with st.container(border=True):
                col1_2, col2_2 = st.columns(2)
                with col1_2:
                    st.metric(f"{option_type} Option Model Price", f"${put_price:.2f}")
                with col2_2:
                    st.metric(f"{greek_model} for {option_type}", f"{theta_put:.3f}")
                    
        with st.container(border=True):
            st.subheader("Put Rho Calculation")
            st.write("Calculate the Rho of a put option given its market price.")
            with st.expander("View Variables that impact **Rho**"):
                st.markdown(
                    """
                    - **$T-t$**: Time to expiration (in years)
                    - **$K$**: Strike price of the option
                    - **$\\sigma$**: Volatility of the underlying asset's returns
                    - **$r$**: Risk-free interest rate
                    - **$q$**: Dividend yield of the underlying asset
                    - **$k$**: Transaction costs (For Leland's model)
                    - **$dt$**: Time delta (For Leland's model)
                    """
                )

            greek_model = "Rho"
            option_type = "Put"
        
            model_type = st.selectbox(
                f"Select Model for {greek_model} Calculation",
                ["Black-Scholes", "Leland's Model"],
                index=0,
                key=f"{greek_model}_put_rho"
            )

            if model_type == "Leland's Model":
                if dt <= 0:
                    st.warning("Please enter a Δ Time (in the sidebar) greater than zero to use Leland's Model.")
                    st.stop()
                call_price, put_price = get_leland_prices(T, K, S, v, r, q, k, dt)
            else:
                call_price, put_price = get_bsm_prices(T, K, S, v, r, q)

            rho_call, rho_put = get_rho(T, K, S, v, r, q, k, dt, model_type)
            # rho is often expressed per 1% change in interest rates, so we divide by 100
            rho_put /= 100
            
            with st.container(border=True):
                col1_2, col2_2 = st.columns(2)
                with col1_2:
                    st.metric(f"{option_type} Option Model Price", f"${put_price:.2f}")
                with col2_2:
                    st.metric(f"{greek_model} for {option_type}", f"{rho_put:.3f}")

