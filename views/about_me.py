import streamlit as st
from PIL import Image
from functions.helper import get_image_as_base64

# --- Page Configuration ---
st.set_page_config(
    page_title="About Nicholas Richter",
    page_icon=":material/person:",
    layout="wide"
)

linkedin_logo_b64 = get_image_as_base64('assets/linkedin.png')
github_logo_b64 = get_image_as_base64('assets/github.png')

# --- Sidebar Styling ---
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }
    </style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.title("Contacts:")

    st.subheader("Email:")
    st.write("Nicholas.Richter.Work@gmail.com")
    st.subheader("Mobile:")
    st.write("+61 432 454 526")

    st.subheader("Socials:")
    col1, col2, col3 = st.columns([1,1,4])
    with col1:
        st.markdown(f"<a href='https://www.linkedin.com/in/nick-r-richter/' target='_blank'><img src='data:image/png;base64,{linkedin_logo_b64}' width='32'></a>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<a href='https://github.com/Nickyrayy' target='_blank'><img src='data:image/png;base64,{github_logo_b64}' width='32'></a>", unsafe_allow_html=True)

    st.divider()
# --- Profile Section ---
col1, col2 = st.columns([0.3, 0.7], gap="small")
with col1:
    try:
        profile_pic = Image.open('assets/profile-pic-v3.png')
        st.image(profile_pic, width=350)
    except FileNotFoundError:
        st.info("Add a profile picture to assets to display an image here.")


with col2:
    st.title("Nicholas Richter")
    st.subheader("Computer Science & Mathematics Student | Monash University")
    st.warning(
        """
        Hi I'm Nick 👋, I am currently pursuing a double degree in Computer Science and Mathematics, with a major in Data Science, at Monash university. My projects focus on the computation and visualisation of complex financial models, the optimisation of hardware in the realm of high-performance computing, and the development of useful and efficient software.
        """
    )
    social_col1, social_col2, social_col_rest = st.columns([1, 1, 20])

    with social_col1:
        if linkedin_logo_b64:
            st.markdown(
                f"<a href='https://www.linkedin.com/in/nick-r-richter/' target='_blank'><img src='data:image/png;base64,{linkedin_logo_b64}' width='32'></a>",
                unsafe_allow_html=True
            )
        else:
            # fallback to text link if image is not found
            st.markdown("[LinkedIn](https://www.linkedin.com/in/nick-r-richter/)")

    with social_col2:
        if github_logo_b64:
            st.markdown(
                f"<a href='https://github.com/Nickyrayy' target='_blank'><img src='data:image/png;base64,{github_logo_b64}' width='32'></a>",
                unsafe_allow_html=True
            )
        else:
            st.markdown("[GitHub](https://github.com/Nickyrayy)")

st.divider()

# --- BSM Project ---
st.header("Featured Project: Black-Scholes Options Pricing Visualisation Tool")
st.warning(
    """
    This interactive dashboard was developed to calculate and visualize the theoretical price of European call and put options. The primary goal was to create an educational tool that demonstrates the impact of market variables on option pricing, including the effect of transaction costs and the effects various variables have on the option's greeks.
    """
)

col1, col2 = st.columns(2, gap="large")

with col1:
    with st.container(border=True):
        st.subheader("Financial Models Implemented")
        st.warning(
            """
            - **Black-Scholes**: Calculated the theoretical price for European call and put options.
            - **Leland's**: Implemented Hayne E. Leland's variation on the volatility calculation to incorporate transaction costs.
            - **Greeks Calculation**: Computed the Greeks (Delta, Gamma, Vega, Theta, Rho) to assess sensitivity of option prices to various factors.
            - **Implied Volatility**: Calculated implied volatility using the Newton-Raphson method.
            """
        )

with col2:
    with st.container(border=True):
        st.subheader("Core Technologies Used")
        st.warning(
            """
            - **Python**: The core programming language for the project.
            - **Streamlit**: Leveraged for building the interactive and user-friendly web interface.
            - **Matplotlib**: Used for plotting the option pricing graphs and visualizing the effects of different parameters.
            - **NumPy**: Used for efficient numerical computation of the models.
            - **SciPy**: Employed for advanced mathematical functions.
            """
        )

st.divider()

# --- Other Projects Section ---
st.header("Additional Projects")

with st.expander("Low-Latency Stock Market Simulation (In Progress)"):
    st.warning(
        """
        I am currently designing and implementing a high-frequency trading (HFT) simulation on FPGA software (GHDL) to explore ultra-low-latency hardware acceleration techniques. This involves developing VHDL modules for core market functions like order book management and matching engines, with a focus on optimizing for parallel execution and minimal clock cycle delay.
        
        **Technologies:** VHDL, FPGA, GTKwave, GHDL.
        """
    )

with st.expander("Component-Level Hardware Diagnostics & Repair"):
    st.warning(
        """
        I established a small-scale operation to procure, diagnose, and repair faulty consumer electronics (primarily Xbox One consoles) at the component level. Using a multimeter, soldering iron, and heat gun, I identify and replace failed components like capacitors and ICs, successfully restoring over 95% of devices to full functionality for a consistent profit.
        
        **Skills:** Soldering, Multimeter Diagnostics, Circuit Analysis.
        """
    )

with st.expander("Cloud-Hosted Secure VPN"):
    st.warning(
        """
        I deployed and configured a personal VPN server on an Oracle Cloud (OCI) instance. This project involved managing firewall rules via the Linux terminal to create a secure network tunnel for personal use.
        
        **Technologies:** Linux, Oracle Cloud (OCI), OpenVPN.
        """
    )
st.divider()

# --- Skills Section ---
st.header("Technical Skills")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.subheader("Languages")
        st.warning(
            """
            - VHDL
            - Python
            - SQL
            - Bash/Shell Scripting
            """
        )

with col2:
    with st.container(border=True):
        st.subheader("Tools & Technologies")
        st.warning(
            """
            - Linux/Unix, Git
            - Oracle Cloud (OCI)
            - GHDL, GTKwave
            - Streamlit, NumPy, Pandas
            """
        )

with col3:
    with st.container(border=True):
        st.subheader("Hardware")
        st.warning(
            """
            - Digital Logic Design
            - Circuit Analysis
            - Soldering
            - Multimeter Diagnostics
            """)