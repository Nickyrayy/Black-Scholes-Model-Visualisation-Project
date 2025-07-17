import streamlit as st
from functions.graph_surface_helper import generate_bsm_surface, generate_leland_surface, generate_bsm_vs_leland_surface
import base64
import os

from functions.computations import (
    get_bsm_prices,
    get_leland_prices,
)


def display_option_surface(title, surface_func, base_args, key_suffix, default_rotation, elevation=None, rotation=None):
    """
    A reusable function to display an option surface plot and its controls.
    This function is a general-purpose plotter.
    """
    with st.container(border=True):
        st.subheader(title)
        plot_placeholder = st.empty()

        # If elevation and rotation are not passed directly, create sliders for them.
        if elevation is None and rotation is None:
            with st.expander("Adjust Plot View"):
                elevation = st.slider('Elevation', 0, 90, 20, 5, key=f"e_{key_suffix}")
                rotation = st.slider('Rotation', 0, 360, value=default_rotation, step=5, key=f"r_{key_suffix}")

        # Construct the full list of arguments for the plotting function
        # The order is based on the computation function signature: (type, elevation, rotation, ...)
        all_args = (base_args[0], elevation, rotation) + base_args[1:]
        
        # Generate the plot figure
        fig = surface_func(*all_args)
        plot_placeholder.pyplot(fig)

def generate_bsm_option_surface(option_type, strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, elevation=None, rotation=None):
    """
    Generates and displays a Black-Scholes option surface.
    This function is specific to the Black-Scholes model.
    """
    # Prepare arguments for the BSM computation function
    bsm_args = (option_type, strike_min, strike_max, maturity_min, maturity_max, S, v, r, q)
    
    # Set a default viewing angle based on the option type
    default_rotation = 330 if option_type == "Call" else 230
    
    display_option_surface(
        title=f"{option_type} Option Surface",
        surface_func=generate_bsm_surface,
        base_args=bsm_args,
        key_suffix=f"bsm_{option_type.lower()}",
        default_rotation=default_rotation,
        elevation=elevation,
        rotation=rotation
    )

def generate_leland_option_surface(option_type, strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt, elevation=None, rotation=None):
    """
    Generates and displays a Leland's Model option surface.
    This function is specific to Leland's model.
    """
    # Leland's model requires time delta (dt) to be greater than zero.
    if not dt > 0:
        st.info(f"To plot the {option_type} surface, please set a Δ Time greater than zero in the sidebar.")
        return

    # Prepare arguments for the Leland computation function
    leland_args = (option_type, strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt)
    
    # Set a default viewing angle based on the option type
    default_rotation = 330 if "Call" in option_type else 230

    display_option_surface(
        title=f"{option_type} Surface",
        surface_func=generate_leland_surface,
        base_args=leland_args,
        key_suffix=f"leland_{option_type.replace(' ', '_').lower()}",
        default_rotation=default_rotation,
        elevation=elevation,
        rotation=rotation
    )

def generate_bsm_vs_leland_option_surface(option_type, strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt, elevation=None, rotation=None):
    """
    Generates and displays a comparison surface between Black-Scholes and Leland's model.
    This function is specific to the BSM vs BSML comparison.
    """
    # Leland's model requires time delta (dt) to be greater than zero.
    if not dt > 0:
        st.warning(f"To plot the {option_type} surface, please set a Δ Time greater than zero in the sidebar.")
        return

    # Prepare arguments for the Leland computation function
    leland_args = (option_type, strike_min, strike_max, maturity_min, maturity_max, S, v, r, q, k, dt)
    
    # Set a default viewing angle based on the option type
    default_rotation = 330 if "Call" in option_type else 230

    display_option_surface(
        title=f"Bsm vs Leland {option_type} Surface",
        surface_func=generate_bsm_vs_leland_surface,
        base_args=leland_args,
        key_suffix=f"bsmVsleland_{option_type.replace(' ', '_').lower()}",
        default_rotation=default_rotation,
        elevation=elevation,
        rotation=rotation
    )

def get_image_as_base64(path):
    """Encodes a local image file into a base64 string for embedding in HTML."""
    if not os.path.exists(path):
        return None
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()
    
def get_greeks_format(T, K, S, v, r, q, k, dt, greek_model, greek_name):
    with st.container(border=True):
            
        model_type = st.selectbox(
            f"Select Model for {greek_name} Calculation",
            ["Black-Scholes", "Leland's Model"],
            index=0,
            key=f"{greek_model}_model_type"
        )

        if model_type == "Leland's Model":
            if dt <= 0:
                st.info("Please enter a Δ Time (in the sidebar) greater than zero to use Leland's Model.")
                st.stop()
            call_price, put_price = get_leland_prices(T, K, S, v, r, q, k, dt)
        else:
            call_price, put_price = get_bsm_prices(T, K, S, v, r, q)
            
        option_type = st.selectbox(
            f"Select Option Type for {greek_name} Calculation",
            ["Call", "Put"],
            index=0,
            key=f"{greek_model}_option_type"
            )
        
        if greek_name == "Implied Volatility":
            option_type_market_price = st.number_input(
                    "Market Price of the Option $",
                    min_value=0.0,
                    value=call_price,
                    format="%.2f",
                    key=f"{greek_model}_market_price"
                )
        else:
            option_type_market_price = None
        
        if option_type == "Call":
            option_price = call_price
        else:
            option_price = put_price


        option_type, greek_output = greek_model(T, K, S, v, r, q, option_type, option_type_market_price)

        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                st.metric(f"{option_type} Option Model Price", f"${option_price:.2f}")
            with col2:
                st.metric(f"{greek_name} for {option_type} Option", f"{greek_output:.2%}")
