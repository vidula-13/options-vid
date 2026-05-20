import numpy as np
from scipy.stats import norm


def _d1(S, K, T, r, sigma):
    return (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))


def _d2(S, K, T, r, sigma):
    return _d1(S, K, T, r, sigma) - sigma * np.sqrt(T)


def call_price(S, K, T, r, sigma):
    """
    Calculate European Call Option Price
    """
    d1 = _d1(S, K, T, r, sigma)
    d2 = _d2(S, K, T, r, sigma)

    call = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

    return float(call)


def put_price(S, K, T, r, sigma):
    """
    Calculate European Put Option Price
    """
    d1 = _d1(S, K, T, r, sigma)
    d2 = _d2(S, K, T, r, sigma)

    put = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return float(put)


# ------------------ GREEKS ------------------

def delta(S, K, T, r, sigma, option_type="call"):
    d1 = _d1(S, K, T, r, sigma)

    if option_type == "call":
        return float(norm.cdf(d1))
    else:
        return float(norm.cdf(d1) - 1)


def gamma(S, K, T, r, sigma):
    d1 = _d1(S, K, T, r, sigma)

    return float(norm.pdf(d1) / (S * sigma * np.sqrt(T)))


def vega(S, K, T, r, sigma):
    d1 = _d1(S, K, T, r, sigma)

    return float(S * norm.pdf(d1) * np.sqrt(T))


# ------------------ TEST ------------------

if __name__ == "__main__":
    # Sample inputs
    S = 1800     # stock price
    K = 1850     # strike price
    T = 0.5      # 6 months
    r = 0.065    # risk-free rate
    sigma = 0.30 # volatility

    call = call_price(S, K, T, r, sigma)
    put = put_price(S, K, T, r, sigma)

    print(f"\nCall Price: {call:.2f}")
    print(f"Put Price: {put:.2f}")

    print("\nGreeks:")
    print(f"Delta (Call): {delta(S, K, T, r, sigma, 'call'):.4f}")
    print(f"Gamma: {gamma(S, K, T, r, sigma):.6f}")
    print(f"Vega: {vega(S, K, T, r, sigma):.2f}")