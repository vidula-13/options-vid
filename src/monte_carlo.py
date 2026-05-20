import numpy as np


def monte_carlo_simulation(S, T, r, sigma, simulations=1000, steps=100):
    """
    Simulate stock price paths using Geometric Brownian Motion
    """

    dt = T / steps
    paths = np.zeros((steps, simulations))
    paths[0] = S

    for t in range(1, steps):
        Z = np.random.standard_normal(simulations)
        paths[t] = paths[t-1] * np.exp(
            (r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z
        )

    return paths


def probability_of_profit(paths, K, option_type="call"):
    """
    Estimate probability of profit at expiry
    """

    final_prices = paths[-1]

    if option_type == "call":
        profitable = final_prices > K
    else:
        profitable = final_prices < K

    return np.mean(profitable)