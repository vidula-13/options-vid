import numpy as np
import pandas as pd


def compute_log_returns(df: pd.DataFrame) -> pd.Series:
    """
    Compute daily log returns from closing prices.

    Parameters:
    ----------
    df : pd.DataFrame
        DataFrame containing 'Close' prices

    Returns:
    -------
    pd.Series
        Log returns
    """

    if "Close" not in df.columns:
        raise ValueError("DataFrame must contain 'Close' column")

    log_returns = np.log(df["Close"] / df["Close"].shift(1))

    return log_returns.dropna()


def compute_volatility(log_returns: pd.Series, trading_days: int = 252) -> float:
    """
    Compute annualized volatility.

    Parameters:
    ----------
    log_returns : pd.Series
        Daily log returns
    trading_days : int
        Number of trading days in a year (default = 252)

    Returns:
    -------
    float
        Annualized volatility
    """

    if len(log_returns) < 30:
        raise ValueError("Not enough data to compute volatility")

    daily_volatility = log_returns.std()

    annualized_volatility = daily_volatility * np.sqrt(trading_days)

    return float(annualized_volatility)


def compute_rolling_volatility(log_returns: pd.Series, window: int = 30) -> pd.Series:
    """
    Compute rolling volatility (useful for visualization).

    Parameters:
    ----------
    log_returns : pd.Series
        Daily log returns
    window : int
        Rolling window size

    Returns:
    -------
    pd.Series
        Rolling volatility
    """

    rolling_vol = log_returns.rolling(window=window).std() * np.sqrt(252)

    return rolling_vol.dropna()


if __name__ == "__main__":
    # Test module
    from src.data_fetch import fetch_stock_data, get_default_ticker

    ticker = get_default_ticker()

    price, df, name = fetch_stock_data(ticker)

    log_returns = compute_log_returns(df)
    volatility = compute_volatility(log_returns)
    rolling_vol = compute_rolling_volatility(log_returns)

    print(f"\nCompany: {name}")
    print(f"Annualized Volatility: {volatility:.2%}")
    print("\nRolling Volatility Sample:")
    print(rolling_vol.head())