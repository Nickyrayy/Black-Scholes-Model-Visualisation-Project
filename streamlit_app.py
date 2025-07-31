import streamlit as st

# Page Setup

about_page = st.Page(
    page="./views/about_me.py",
    title="About Me & Project Outline",
    icon=":material/person:",
    default=True
)

bsm_page = st.Page(
    page="./views/bsm.py",
    title="Black-Scholes Model ",
    icon=":material/functions:"
)

bsm_info = st.Page(
    page="./views/bsm_info.py",
    title="Black-Scholes Model Information",
    icon=":material/book_ribbon:"
)

pg = st.navigation(
    {
        "Info":[about_page,bsm_info],
        "Models":[bsm_page],
    }
)

pg.run()