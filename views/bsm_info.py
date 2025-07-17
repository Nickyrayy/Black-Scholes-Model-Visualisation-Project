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
    st.latex(r'''Le = \sqrt{\frac{2}{\pi}} \cdot \frac{k}{\sigma \sqrt{\Delta t}}''')
    st.markdown("""
    - **$k$**: Round-trip transaction cost (as a percentage of the asset's value).
    - **$\\sigma$**: The original, unadjusted volatility of the underlying.
    - **$\\Delta t$**: The time interval between portfolio re-hedges (in years). A smaller $\\Delta t$ implies more frequent hedging.
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

col1, col2, col3 = st.columns([1,3,1])
with col2:
    st.title("Option Pricing Models: A Brief Technical Overview")
    st.info("""
        This page provides an overview of the **financial models** used in this application for option pricing.
        Understanding these models, their assumptions, and their differences is key to interpreting the results.
    """)

    st.divider()

    # --- Black-Scholes Model Section ---
    with st.container(border=True):
        st.header("The Black-Scholes-Merton (BSM) Model")
        st.markdown("""
            The **Black-Scholes-Merton model** is a cornerstone of modern financial theory. Developed by Fischer Black, Myron Scholes,
            and Robert Merton (who was awarded the Nobel Prize in Economics for it in 1997), it provides a mathematical formula
            for calculating the theoretical price of European-style options. The model's key insight is that one can perfectly
            hedge an option by buying and selling the underlying asset in a specific way, eliminating risk. This leads to a
            single, fair price for the option.

            However, this is based on the assumption of a "perfect" or "frictionless" market with a specific set of conditions.
        """)

        with st.expander("See Key Assumptions"):
            st.markdown("""
            - **European Options:** The options can only be exercised at the expiration date.
            - **No Dividends:** The underlying stock does not pay dividends during the option's life (though the model can be adjusted for them).
            - **Efficient Markets:** Market movements are random and cannot be predicted (Random Walk Theory).
            - **No Transaction Costs:** There are no fees or costs associated with buying or selling the option or the underlying asset. This is a critical assumption that the Leland model addresses.
            - **Constant Volatility and Risk-Free Rate:** The volatility of the underlying asset and the risk-free interest rate are known and constant over the option's life.
            - **Lognormal Distribution:** The returns on the underlying asset are lognormally distributed.
            """)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Call Option Price (C)")
            st.latex(r'''
            C(S, t) = S N(d_1) - K e^{-r(T-t)} N(d_2)
            ''')

        with col2:
            st.markdown("#### Put Option Price (P)")
            st.latex(r'''
            P(S, t) = K e^{-r(T-t)} N(-d_2) - S N(-d_1)
            ''')

        with st.expander("View the Black-Scholes Formulas"):

            st.markdown("Where:")
            st.latex(r'''
            d_1 = \frac{\ln(\frac{S}{K}) + (r + \frac{\sigma^2}{2})(T-t)}{\sigma\sqrt{T-t}}
            ''')
            st.latex(r'''
            d_2 = d_1 - \sigma\sqrt{T-t}
            ''')

            st.markdown(
                """
                - **$S$**: Current price of the underlying asset
                - **$K$**: Strike price of the option
                - **$T-t$**: Time to expiration (in years)
                - **$r$**: Risk-free interest rate
                - **$\\sigma$**: Volatility of the underlying asset's returns
                - **$N(d)$**: The cumulative distribution function of the standard normal distribution
                """
            )

    # --- Leland's Model Section ---
    with st.container(border=True):
        st.header("Leland's Model: Incorporating Transaction Costs")
        st.markdown("""
            One of the most significant limitations of the Black-Scholes model is its assumption of a frictionless market. In practice, the continuous portfolio rebalancing required for a perfect delta hedge would lead to infinite transaction costs.

            Hayne Leland's 1985 model addresses this by providing a practical solution. Instead of fundamentally altering the BSM equation, Leland showed that the effect of transaction costs could be approximated by adjusting a single, critical input: **volatility**. The logic is that transaction costs add to the risk of hedging, and this increased risk is analogous to an increase in the asset's volatility. By 'inflating' the volatility, the model charges a higher premium for the option to cover anticipated transaction costs.
        """)

        with st.expander("See How the Leland Model Works"):
            st.markdown("""
            The application of the model is a two-step process: first, calculate an adjusted volatility that accounts for transaction costs, and second, use this adjusted volatility in the standard Black-Scholes formula.
            """)
            st.markdown("#### Step 1: Calculate the Adjusted Volatility ($\\sigma_{adj}$)")
            st.markdown("The core of the adjustment is the **Leland Number (Le)**, which quantifies the impact of transaction costs.")
            st.latex(r'''
            Le = \sqrt{\frac{2}{\pi}} \times \frac{k}{\sigma \sqrt{\Delta t}}
            ''')
            st.markdown(
                """
                - **$k$**: Round-trip transaction cost as a percentage of the asset price.
                - **$\\sigma$**: Original volatility of the underlying asset.
                - **$\\Delta t$**: The time interval between portfolio re-hedges (e.g., daily would be 1/252).
                """
            )

            st.markdown("The adjusted volatility squared is then calculated. A higher Leland Number leads to a larger adjustment.")
            st.latex(r'''
            \sigma_{adj}^2 = \sigma^2 \left(1 + Le\right)
            ''')
            st.markdown(r"""
                *(Note: The full formula includes a term, $\text{sign}(N'(d_1))$, which is always positive for standard options, simplifying the equation for practical use.)*
            """)

            st.markdown("#### Step 2: Apply Adjusted Volatility to the BSM Formula")
            st.markdown(r"""
            Once $\sigma_{adj}$ is calculated, it is simply substituted into the standard Black-Scholes pricing formula in place of the original volatility, $\sigma$. All other inputs ($S, K, r, T-t$) remain the same.
            """)

        with st.expander("View Practical Implications and Limitations"):
            st.markdown("##### Hedging Strategies")
            st.markdown("""
            - **Discrete Rebalancing:** The model explicitly acknowledges that hedging is not continuous. The choice of the rebalancing interval, $\\Delta t$, is a critical decision. A shorter interval leads to a better hedge but incurs higher transaction costs, which is reflected in a higher adjusted volatility and a more expensive option price.
            - **Wider Hedging Bands:** The increased volatility effectively creates a "band" around the theoretical BSM delta. A trader using this model would only rebalance their position when the portfolio's delta moves outside of this implicit band, reducing trading frequency and costs.
            """)

            st.markdown("##### Model Limitations")
            st.markdown("""
            - **Approximation:** The Leland model is an approximation. It may underestimate the true cost of re-hedging after a large, sudden price jump.
            - **Ex-ante Cost Estimation:** The model calculates the *expected* transaction cost at the start. The *actual* costs incurred will depend on the path the asset price takes over the life of the option.
            - **No Unique Price:** Because the adjusted volatility depends on the chosen rebalancing frequency ($\\Delta t$), there is no single "correct" price, but rather a price that is consistent with a specific hedging strategy.
            """)

    st.info("In conclusion, the Leland model provides a practical method for incorporating transaction costs into option pricing. By adjusting volatility, it offers a more conservative and realistic valuation, acknowledging that maintaining a hedge is not a cost-free exercise.")
