import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns

def compute_option_price(spot, strike, rate, maturity, vol, option_type="call"):
    "Calculate the Black-Scholes price for a call or put option"
    d1 = (np.log(spot/strike) + (rate + vol**2/2) * maturity) / (vol * np.sqrt(maturity))
    d2 = d1 - vol * np.sqrt(maturity)

    try:
        if option_type == "call":
            price = spot * norm.cdf(d1) - strike * np.exp(-rate * maturity) * norm.cdf(d2)
        elif option_type == "put":
            price = strike * np.exp(-rate * maturity) * norm.cdf(-d2) - spot * norm.cdf(-d1)

        return price
    except:
        st.sidebar.error("Ensure all parameters are correctly entered!")

def compute_delta(spot, strike, rate, maturity, vol, option_type="call"):
    "Calculate the option's delta"
    d1 = (np.log(spot/strike) + (rate + vol**2/2) * maturity) / (vol * np.sqrt(maturity))
    
    try:
        if option_type == "call":
            delta = norm.cdf(d1)
        elif option_type == "put":
            delta = -norm.cdf(-d1)

        return delta
    except:
        st.sidebar.error("Ensure all parameters are correctly entered!")

def compute_gamma(spot, strike, rate, maturity, vol):
    "Calculate the option's gamma"
    d1 = (np.log(spot/strike) + (rate + vol**2/2) * maturity) / (vol * np.sqrt(maturity))
    
    try:
        gamma = norm.pdf(d1) / (spot * vol * np.sqrt(maturity))
        return gamma
    except:
        st.sidebar.error("Ensure all parameters are correctly entered!")

def compute_theta(spot, strike, rate, maturity, vol, option_type="call"):
    "Calculate the option's theta"
    d1 = (np.log(spot/strike) + (rate + vol**2/2) * maturity) / (vol * np.sqrt(maturity))
    d2 = d1 - vol * np.sqrt(maturity)
    
    try:
        if option_type == "call":
            theta = - (spot * norm.pdf(d1) * vol) / (2 * np.sqrt(maturity)) - rate * strike * np.exp(-rate*maturity) * norm.cdf(d2)
        elif option_type == "put":
            theta = - (spot * norm.pdf(d1) * vol) / (2 * np.sqrt(maturity)) + rate * strike * np.exp(-rate*maturity) * norm.cdf(-d2)
        return theta / 365  # Annualize theta
    except:
        st.sidebar.error("Ensure all parameters are correctly entered!")

def compute_vega(spot, strike, rate, maturity, vol):
    "Calculate the option's vega"
    d1 = (np.log(spot/strike) + (rate + vol**2/2) * maturity) / (vol * np.sqrt(maturity))
    
    try:
        vega = spot * np.sqrt(maturity) * norm.pdf(d1) * 0.01
        return vega
    except:
        st.sidebar.error("Ensure all parameters are correctly entered!")

def compute_rho(spot, strike, rate, maturity, vol, option_type="call"):
    "Calculate the option's rho"
    d2 = (np.log(spot/strike) + (rate - vol**2/2) * maturity) / (vol * np.sqrt(maturity))
    
    try:
        if option_type == "call":
            rho = 0.01 * strike * maturity * np.exp(-rate*maturity) * norm.cdf(d2)
        elif option_type == "put":
            rho = -0.01 * strike * maturity * np.exp(-rate*maturity) * norm.cdf(-d2)
        return rho
    except:
        st.sidebar.error("Ensure all parameters are correctly entered!")

# Streamlit page configuration
st.set_page_config(page_title="Option Pricing & Greeks")

st.sidebar.header("Input Parameters")
interest_rate = st.sidebar.number_input("Risk-Free Rate", min_value=0.000, max_value=1.000, step=0.001, value=0.030)
spot_price = st.sidebar.number_input("Underlying Asset Price", min_value=1.00, step=0.10, value=30.00)
strike_price = st.sidebar.number_input("Strike Price", min_value=1.00, step=0.10, value=50.00)
days_to_maturity = st.sidebar.number_input("Days Until Expiry", min_value=1, step=1, value=250)
volatility = st.sidebar.number_input("Volatility", min_value=0.000, max_value=1.000, step=0.01, value=0.30)
option_type_selection = st.sidebar.selectbox("Option Type", ["Call", "Put"])

maturity_time = days_to_maturity / 365
option_type = "call" if option_type_selection == "Call" else "put"

# Calculating for multiple spot prices
spot_prices_range = np.arange(0, spot_price + 50 + 1)

option_prices = [compute_option_price(spot, strike_price, interest_rate, maturity_time, volatility, option_type) for spot in spot_prices_range]
deltas = [compute_delta(spot, strike_price, interest_rate, maturity_time, volatility, option_type) for spot in spot_prices_range]
gammas = [compute_gamma(spot, strike_price, interest_rate, maturity_time, volatility) for spot in spot_prices_range]
thetas = [compute_theta(spot, strike_price, interest_rate, maturity_time, volatility, option_type) for spot in spot_prices_range]
vegas = [compute_vega(spot, strike_price, interest_rate, maturity_time, volatility) for spot in spot_prices_range]
rhos = [compute_rho(spot, strike_price, interest_rate, maturity_time, volatility, option_type) for spot in spot_prices_range]

# Set style for plots
sns.set_style("whitegrid")

# Plotting the results
fig1, ax1 = plt.subplots()
sns.lineplot(x=spot_prices_range, y=option_prices, ax=ax1)
ax1.set_ylabel('Option Price')
ax1.set_xlabel("Underlying Asset Price")
ax1.set_title("Option Price")

fig2, ax2 = plt.subplots()
sns.lineplot(x=spot_prices_range, y=deltas, ax=ax2)
ax2.set_ylabel('Delta')
ax2.set_xlabel("Underlying Asset Price")
ax2.set_title("Delta")

fig3, ax3 = plt.subplots()
sns.lineplot(x=spot_prices_range, y=gammas, ax=ax3)
ax3.set_ylabel('Gamma')
ax3.set_xlabel("Underlying Asset Price")
ax3.set_title("Gamma")

fig4, ax4 = plt.subplots()
sns.lineplot(x=spot_prices_range, y=thetas, ax=ax4)
ax4.set_ylabel('Theta')
ax4.set_xlabel("Underlying Asset Price")
ax4.set_title("Theta")

fig5, ax5 = plt.subplots()
sns.lineplot(x=spot_prices_range, y=vegas, ax=ax5)
ax5.set_ylabel('Vega')
ax5.set_xlabel("Underlying Asset Price")
ax5.set_title("Vega")

fig6, ax6 = plt.subplots()
sns.lineplot(x=spot_prices_range, y=rhos, ax=ax6)
ax6.set_ylabel('Rho')
ax6.set_xlabel("Underlying Asset Price")
ax6.set_title("Rho")

fig1.tight_layout()
fig2.tight_layout()
fig3.tight_layout()
fig4.tight_layout()
fig5.tight_layout()
fig6.tight_layout()

# Display in Streamlit
st.markdown("<h2 align='center'>Black-Scholes Option Pricing Calculator</h2>", unsafe_allow_html=True)
st.header("")
st.markdown("<h3 align='center'>Option Prices and Greeks</h3>", unsafe_allow_html=True)
st.header("")
col1, col2, col3, col4, col5 = st.columns(5)
col2.metric("Call Price", str(round(compute_option_price(spot_price, strike_price, interest_rate, maturity_time, volatility, "call"), 3)))
col4.metric("Put Price", str(round(compute_option_price(spot_price, strike_price, interest_rate, maturity_time, volatility, "put"), 3)))

bcol1, bcol2, bcol3, bcol4, bcol5 = st.columns(5)
bcol1.metric("Delta", str(round(compute_delta(spot_price, strike_price, interest_rate, maturity_time, volatility, "call"), 3)))
bcol2.metric("Gamma", str(round(compute_gamma(spot_price, strike_price, interest_rate, maturity_time, volatility), 3)))
bcol3.metric("Theta", str(round(compute_theta(spot_price, strike_price, interest_rate, maturity_time, volatility, "call"), 3)))
bcol4.metric("Vega", str(round(compute_vega(spot_price, strike_price, interest_rate, maturity_time, volatility), 3)))
bcol5.metric("Rho", str(round(compute_rho(spot_price, strike_price, interest_rate, maturity_time, volatility, "call"), 3)))

st.header("")
st.markdown("<h3 align='center'>Greeks Visualization</h3>", unsafe_allow_html=True)
st.header("")
st.pyplot(fig1)
st.pyplot(fig2)
st.pyplot(fig3)
st.pyplot(fig4)
st.pyplot(fig5)
st.pyplot(fig6)
