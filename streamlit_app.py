import streamlit as st


# Page Setup

about_page = st.Page(
    page="./views/about_me.py",
    title="About Me",
    icon=":material/person:",
    default=True,
)

bsm_page = st.Page(
    page="./views/bsm.py",
    title="Black-Scholes Model ",
    icon=":material/functions:",
)

pg = st.navigation(
    {
        "info":[about_page],
        "Models":[bsm_page],
    }
)

st.logo("assets/black-scholes-model-high-resolution-logo.png")

pg.run()