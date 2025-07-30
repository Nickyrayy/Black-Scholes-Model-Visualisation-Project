import streamlit as st


# Page Setup

about_page = st.Page(
    page="./views/about_me.py",
    title="About Me",
    icon=":material/person:",
)

bsm_page = st.Page(
    page="./views/bsm.py",
    title="Black-Scholes Model ",
    icon=":material/functions:",
    default=True
)

bsm_info = st.Page(
    page="./views/bsm_info.py",
    title="Black-Scholes Model Information",
    icon=":material/functions:"
)

pg = st.navigation(
    {
        "info":[about_page,bsm_info],
        "Models":[bsm_page],
    }
)
# doesnt show for some reason
st.logo("assets/black-scholes-model-high-resolution-logo.png")

pg.run()