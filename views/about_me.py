import streamlit as st
from PIL import Image
from functions.helper import get_image_as_base64
# --- Page Configuration ---
# Use st.set_page_config to set the page title, icon, and layout.
st.set_page_config(
    page_title="About Nicholas Richter",
    page_icon="�",
    layout="wide"
)

# --- Profile Section ---
# Using columns to place an image next to the introduction.
col1, col2 = st.columns([0.3, 0.7], gap="large")
with col1:
    # It's a good practice to use a professional-looking, square image.
    # Make sure to replace 'assets/profile_pic.png' with the actual path to your image.
    try:
        profile_pic = Image.open('assets/profile_pic.png')
        st.image(profile_pic, width=230)
    except FileNotFoundError:
        st.info("Add a profile picture to 'assets/profile_pic.png' to display an image here.")


with col2:
    st.title("Nicholas Richter")
    st.subheader("Computer Science & Mathematics Student | Monash University")
    st.write(
        """
        I am a driven and analytical student pursuing a double degree in Computer Science and Mathematics, with a major in Data Science. My work focuses on the intersection of complex financial models, high-performance computing, and intuitive software design. This portfolio showcases my ability to transform theoretical concepts into practical, hands-on applications.
        """
    )
    # Adding links to your professional profiles.
    # Create columns for the social links
    social_col1, social_col2, social_col_rest = st.columns([1, 1, 20])

    # Get base64 encoded strings for logos
    linkedin_logo_b64 = get_image_as_base64('assets/linkedin.png')
    github_logo_b64 = get_image_as_base64('assets/github.png')

    with social_col1:
        if linkedin_logo_b64:
            st.markdown(
                f"<a href='https://www.linkedin.com/in/nick-r-richter/' target='_blank'><img src='data:image/png;base64,{linkedin_logo_b64}' width='32'></a>",
                unsafe_allow_html=True
            )
        else:
            # Fallback to text link if image is not found
            st.markdown("[🔗 LinkedIn](https://www.linkedin.com/in/nick-r-richter/)")

    with social_col2:
        if github_logo_b64:
            st.markdown(
                f"<a href='https://github.com/Nickyrayy' target='_blank'><img src='data:image/png;base64,{github_logo_b64}' width='32'></a>",
                unsafe_allow_html=True
            )
        else:
            st.markdown("[🐙 GitHub](https://github.com/Nickyrayy)")

st.markdown("---")

# --- Project Emphasis Section ---
st.header("Featured Project: Black-Scholes Options Pricing Visualisation Tool")
st.markdown(
    """
    This interactive dashboard was developed to calculate and visualize the theoretical price of European call and put options. The primary goal was to create an educational tool that clearly demonstrates the impact of market variables on option pricing, including the nuanced effect of transaction costs.
    """
)

# Using columns to detail the project's features, directly referencing the app's functionality.
col1, col2 = st.columns(2, gap="large")

with col1:
    with st.container(border=True):
        st.subheader("Financial Models Implemented")
        st.markdown(
            """
            - **Black-Scholes Model**: Calculated the theoretical price for European call and put options.
            - **Leland's Transaction Cost Model**: Implemented Hayne E. Leland's variation on the volatility calculation to incorporate transaction costs.
            """
        )

with col2:
    with st.container(border=True):
        st.subheader("Core Technologies Used")
        st.markdown(
            """
            - **Python**: The core programming language for the project.
            - **Streamlit**: Leveraged for building the interactive and user-friendly web interface.
            - **NumPy & Matplotlib**: Used for efficient numerical computation and creating the data visualizations.
            """
        )

st.markdown("---")

# --- Other Projects Section ---
st.header("Additional Projects")

with st.expander("🚀 Low-Latency Stock Market Simulation (In Progress)"):
    st.markdown(
        """
        I am currently designing and implementing a high-frequency trading (HFT) simulation on FPGA software (GHDL) to explore ultra-low-latency hardware acceleration techniques. This involves developing VHDL modules for core market functions like order book management and matching engines, with a focus on optimizing for parallel execution and minimal clock cycle delay.
        
        **Technologies:** VHDL, FPGA, GTKwave, GHDL.
        """
    )

with st.expander("🔧 Component-Level Hardware Diagnostics & Repair"):
    st.markdown(
        """
        I established a small-scale operation to procure, diagnose, and repair faulty consumer electronics (primarily Xbox One consoles) at the component level. Using a multimeter, soldering iron, and heat gun, I identify and replace failed components like capacitors and ICs, successfully restoring over 95% of devices to full functionality for a consistent profit.
        
        **Skills:** Soldering, Multimeter Diagnostics, Circuit Analysis.
        """
    )

with st.expander("☁️ Cloud-Hosted Secure VPN"):
    st.markdown(
        """
        I deployed and configured a personal VPN server on an Oracle Cloud (OCI) instance. This project involved managing firewall rules via the Linux terminal to create a secure network tunnel for personal use.
        
        **Technologies:** Linux, Oracle Cloud (OCI), OpenVPN.
        """
    )
st.markdown("---")

# --- Skills Section ---
st.header("Technical Skills")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.subheader("Languages")
        st.markdown(
            """
            - VHDL
            - Python
            - SQL
            """
        )
with col2:
    with st.container(border=True):
        st.subheader("Tools & Technologies")
        st.markdown(
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
        st.markdown(
            """
            - Digital Logic Design
            - Circuit Analysis
            - Soldering
            - Multimeter Diagnostics
            """)