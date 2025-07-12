import streamlit as st
import sys
sys.path.append('views')

from bsm_model import BlackScholes

st.set_page_config(
    page_title="Black-Scholes Model",
    page_icon=":material/functions:",
    layout="wide",  # wide or centered
    initial_sidebar_state="expanded"

)

