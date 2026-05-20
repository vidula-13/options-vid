import numpy as np
import matplotlib.pyplot as plt


# ------------------ STRATEGY SELECTION ------------------

def get_strategy(outlook: str) -> str:
    """
    Return strategy based on market outlook
    """
    outlook = outlook.lower()

    if outlook == "bullish":
        return "Long Call"
    elif outlook == "bearish":
        return "Long Put"
    elif outlook == "neutral":
        return "Straddle"
    else:
        raise ValueError("Invalid outlook. Choose bullish, bearish, or neutral.")


# ------------------ PAYOFF FUNCTIONS ------------------

def call_payoff(S, K, premium):
    return np.maximum(S - K, 0) - premium


def put_payoff(S, K, premium):
    return np.maximum(K - S, 0) - premium


def straddle_payoff(S, K, call_premium, put_premium):
    return call_payoff(S, K, call_premium) + put_payoff(S, K, put_premium)


# ------------------ PLOTTING ------------------

def plot_payoff(current_price, K, call_price, put_price, strategy_name):
    """
    Plot payoff diagram
    """

    # Price range (important for visualization)
    price_range = np.linspace(0.5 * current_price, 1.5 * current_price, 100)

    if strategy_name == "Long Call":
        payoff = call_payoff(price_range, K, call_price)

    elif strategy_name == "Long Put":
        payoff = put_payoff(price_range, K, put_price)

    elif strategy_name == "Straddle":
        payoff = straddle_payoff(price_range, K, call_price, put_price)

    else:
        raise ValueError("Invalid strategy")

    # Plot
    plt.figure(figsize=(8, 5))
    plt.plot(price_range, payoff, label=strategy_name)
    plt.axhline(0)  # break-even line
    plt.axvline(current_price, linestyle="--", label="Current Price")

    plt.title(f"{strategy_name} Payoff")
    plt.xlabel("Stock Price at Expiry")
    plt.ylabel("Profit / Loss")
    plt.legend()
    plt.grid()

    return plt


# ------------------ TEST ------------------

if __name__ == "__main__":
    current_price = 1800
    K = 1800
    call_price = 100
    put_price = 90

    strategy = get_strategy("neutral")

    print(f"Strategy: {strategy}")

    plot = plot_payoff(current_price, K, call_price, put_price, strategy)
    plot.show()