import streamlit as st

def display_option_surface(title, surface_func, base_args, key_suffix, default_rotation, elevation=None, rotation=None):
    """
    A reusable function to display an option surface plot and its controls.
    """
    st.subheader(title)
    plot_placeholder = st.empty()

    if elevation is None and rotation is None:
        with st.expander("Adjust Plot View"):
            elevation = st.slider('Elevation', 0, 90, 20, 5, key=f"e_{key_suffix}")
            rotation = st.slider('Rotation', 0, 360, value=default_rotation, step=5, key=f"r_{key_suffix}")

    # Construct the full list of arguments for the plotting function
    # The order is based on the original function signature: (type, elevation, rotation, ...)
    all_args = (base_args[0], elevation, rotation) + base_args[1:]
    
    fig = surface_func(*all_args)
    plot_placeholder.pyplot(fig)