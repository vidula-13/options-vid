import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import matplotlib.pyplot as plt

from src.data_fetch import fetch_stock_data, get_risk_free_rate
from src.volatility import compute_log_returns, compute_volatility, compute_rolling_volatility
from src.black_scholes import call_price, put_price, delta, gamma, vega
from src.strategy import get_strategy, plot_payoff
from src.monte_carlo import monte_carlo_simulation, probability_of_profit


# ------------------ PAGE CONFIG ------------------

st.set_page_config(page_title="Options Strategy Analyzer", layout="wide")


# ------------------ CUSTOM UI ------------------

st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.block-container {
    padding-top: 2rem;
}
[data-testid="metric-container"] {
    background-color: #161b22;
    border: 1px solid #30363d;
    padding: 15px;
    border-radius: 10px;
}
h1 {
    color: #58a6ff;
}
h2, h3 {
    color: #58a6ff;
}
section[data-testid="stSidebar"] {
    background-color: #161b22;
}
button[kind="primary"] {
    background-color: #238636;
    border-radius: 8px;
    height: 3em;
    width: 100%;
    font-weight: 600;
}
label, p, div {
    color: #c9d1d9;
}
</style>
""", unsafe_allow_html=True)


# ------------------ HEADER ------------------

st.markdown("""
<h1>Options Strategy Analyzer</h1>
<p style='color: #8b949e;'>
Quantitative analysis of derivatives using pricing models, volatility metrics, and simulation
</p>
""", unsafe_allow_html=True)

st.markdown("---")


# ------------------ SIDEBAR ------------------

with st.sidebar:
    st.header("Input Parameters")

    ticker = st.text_input("Stock Ticker", value="ADANIENT.NS")
    strike_price = st.number_input("Strike Price", min_value=1.0, value=1800.0)

    outlook = st.selectbox("Market Outlook", ["bullish", "bearish", "neutral"])
    time_to_expiry = st.slider("Time to Expiry (years)", 0.1, 2.0, 0.5)

    analyze = st.button("Run Analysis")


# ------------------ MAIN ------------------

if analyze:

    try:
        current_price, df, company_name = fetch_stock_data(ticker)

        log_returns = compute_log_returns(df)
        sigma = compute_volatility(log_returns)
        rolling_vol = compute_rolling_volatility(log_returns)

        is_indian = ticker.endswith(".NS")
        r = get_risk_free_rate(is_indian)

        call = call_price(current_price, strike_price, time_to_expiry, r, sigma)
        put = put_price(current_price, strike_price, time_to_expiry, r, sigma)

        strategy_name = get_strategy(outlook)

        # ------------------ METRICS ------------------

        st.markdown("### Market Metrics")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Price", f"₹{current_price:.2f}")
        col2.metric("Volatility", f"{sigma:.2%}")
        col3.metric("Call Value", f"₹{call:.2f}")
        col4.metric("Put Value", f"₹{put:.2f}")

        st.markdown("---")

        # ------------------ GREEKS ------------------

        st.markdown("### Greeks Analysis")

        col1, col2, col3 = st.columns(3)

        col1.metric("Delta", f"{delta(current_price, strike_price, time_to_expiry, r, sigma):.4f}")
        col2.metric("Gamma", f"{gamma(current_price, strike_price, time_to_expiry, r, sigma):.6f}")
        col3.metric("Vega", f"{vega(current_price, strike_price, time_to_expiry, r, sigma):.2f}")

        # ------------------ INSIGHT ------------------

        if sigma > 0.4:
            st.error("High volatility regime detected. Elevated uncertainty in pricing.")
        elif sigma < 0.2:
            st.warning("Low volatility environment. Reduced option premiums.")
        else:
            st.success("Moderate volatility. Balanced market conditions.")

        st.markdown("---")

        # ------------------ STRATEGY ------------------

        st.markdown("### Strategy")

        st.write(f"Recommended Strategy: **{strategy_name}**")

        st.markdown("---")

        # ------------------ VOLATILITY ------------------

        st.markdown("### Volatility Trend")

        fig1, ax1 = plt.subplots()
        ax1.plot(rolling_vol)
        ax1.set_title("Rolling Volatility (30-day)")
        ax1.grid()

        st.pyplot(fig1)

        # ------------------ PAYOFF ------------------

        st.markdown("### Payoff Analysis")

        fig2 = plot_payoff(current_price, strike_price, call, put, strategy_name)
        st.pyplot(fig2)

        # ------------------ MONTE CARLO ------------------

        st.markdown("### Monte Carlo Simulation")

        paths = monte_carlo_simulation(current_price, time_to_expiry, r, sigma)

        fig3, ax3 = plt.subplots()

        for i in range(40):
            ax3.plot(paths[:, i], linewidth=0.6)

        ax3.set_title("Simulated Price Paths")
        ax3.grid()

        st.pyplot(fig3)

        # ------------------ PROBABILITY ------------------

        st.markdown("### Probability of Profit")

        prob_call = probability_of_profit(paths, strike_price, "call")
        prob_put = probability_of_profit(paths, strike_price, "put")

        col1, col2 = st.columns(2)

        col1.metric("Call Probability", f"{prob_call:.2%}")
        col2.metric("Put Probability", f"{prob_put:.2%}")

        # ------------------ FOOTER ------------------

        st.markdown("---")
        st.markdown(
            "<p style='text-align:center; color: #8b949e;'>Quantitative Finance Dashboard • Streamlit Interface</p>",
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error(f"Error: {e}")