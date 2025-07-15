import streamlit as st
from functions.computations import generate_bsm_surface, generate_leland_surface

def display_option_surface(title, surface_func, base_args, key_suffix, default_rotation, elevation=None, rotation=None):
    """
    A reusable function to display an option surface plot and its controls.
    This function is a general-purpose plotter.
    """
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
        st.warning(f"To plot the {option_type} surface, please set a Δ Time greater than zero in the sidebar.")
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
