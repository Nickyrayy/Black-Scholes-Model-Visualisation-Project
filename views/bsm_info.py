import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="About the Models",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Header and Introduction ---
st.title("Option Pricing Models: A Brief Technical Overview")
st.info(
    """
    This page details the various **option pricing models** used in this application. 
    A solid grasp of their underlying assumptions and mathematical frameworks is crucial for accurately interpreting the option pricing results.
    """,
    icon="ℹ️"
)

st.markdown("---")

# --- Black-Scholes-Merton Model Section ---
st.header("The Black-Scholes-Merton (BSM) Model")

with st.container(border=True):
    st.markdown("""
    The **Black-Scholes-Merton (BSM) model** is a foundational framework in financial engineering. Developed by Fischer Black, Myron Scholes, and Robert Merton, it provides a differential equation that can be solved to give a theoretical price for European-style options. The model's elegance lies in its closed-form solution, which requires a set of simplifying assumptions about the market.
    """)

    with st.expander("**Key Assumptions of the BSM Model**"):
        st.markdown("""
        - **Option Style:** Applicable only to **European options**, which can be exercised solely at expiration.
        - **Dividends:** The underlying asset pays no dividends during the option's life. (The model can be adjusted to account for them).
        - **Market Dynamics:** Market movements are unpredictable and follow a Geometric Brownian Motion with constant drift and volatility. This is often termed the "Random Walk" theory.
        - **Frictionless Market:** No transaction costs or taxes are involved in buying or selling assets. (This is handled by Hayne E. Leland's variation on the volatility calculation to incorporate transaction costs.)
        - **Constant Parameters:** The risk-free interest rate and the volatility of the underlying asset are known and remain constant throughout the option's life.
        - **Distribution of Returns:** Returns on the underlying asset are lognormally distributed.
        """)

    st.subheader("BSM Pricing Formulas")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Call Option Price (C)")
        st.latex(r'''C(S_t, t) = S_t N(d_1) - K e^{-r(T-t)} N(d_2)''')

    with col2:
        st.markdown("#### Put Option Price (P)")
        st.latex(r'''P(S_t, t) = K e^{-r(T-t)} N(-d_2) - S_t N(-d_1)''')
    
    with st.expander("**Formula Parameters Explained**"):
        st.latex(r'''d_1 = \frac{\ln(\frac{S_t}{K}) + (r + \frac{\sigma^2}{2})(T-t)}{\sigma\sqrt{T-t}}''')
        st.latex(r'''d_2 = d_1 - \sigma\sqrt{T-t}''')
        st.markdown("""
        - **$S_t$**: Current price of the underlying asset.
        - **$K$**: Strike price of the option.
        - **$T-t$**: Time to expiration (in years).
        - **$r$**: Risk-free interest rate (annualized).
        - **$\\sigma$**: Volatility of the underlying asset's returns.
        - **$N(d)$**: The cumulative distribution function (CDF) of the standard normal distribution.
        """)
        
st.markdown("---")

# --- Leland's Model Section ---
st.header("Leland's Model with Transaction Costs")

with st.container(border=True):
    st.markdown("""
    A primary critique of the BSM model is its "frictionless market" assumption. In reality, dynamically hedging an option portfolio incurs transaction costs. **Hayne Leland's 1985 model** extends the BSM framework by incorporating these costs, offering a more realistic valuation.
    
    The model's core idea is to adjust the volatility term in the BSM formula to account for the additional variance created by hedging in the presence of costs.
    """)

    st.subheader("Adjusting Volatility for Hedging Costs")
    
    st.markdown("#### The Leland Number (Le)")
    st.markdown("The impact of transaction costs is quantified by the **Leland Number**, which modifies the volatility based on the cost per transaction and the hedging frequency.")
    st.latex(r'''Le = \sqrt{\frac{2}{\pi}} \cdot \frac{k}{\sigma \sqrt{\delta t}}''')
    st.markdown("""
    - **$k$**: Round-trip transaction cost (as a percentage of the asset's value).
    - **$\\sigma$**: The original, unadjusted volatility of the underlying.
    - **$\\delta t$**: The time interval between portfolio re-hedges (in years). A smaller $\\delta t$ implies more frequent hedging.
    """)

#--- Adjusted Volatility Calculation ---

with st.container(border=True):
    st.subheader("Adjusted Volatility Calculation")

    st.markdown("#### Adjusted Volatility Formula")
    st.markdown("The Leland Number is then used to calculate an adjusted volatility squared ($\\sigma_{adj}^2$):")
    st.latex(r'''\sigma_{adj}^2 = \sigma^2 \left(1 + Le \cdot \text{sign}(\Gamma) \right)''')
    st.markdown(r"""
    This adjusted volatility, $\sigma_{adj}$, is then substituted back into the standard BSM formulas to derive the option price. Since the option's Gamma ($\Gamma$) is positive for standard long call/put positions, this adjustment effectively increases the asset's volatility, leading to higher option premiums.
    """)