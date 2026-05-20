import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker: str, period: str = "5y", interval: str = "1d") -> tuple:
    """
    Fetch stock data and return current price, dataframe, and company name.
    """

    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval, auto_adjust=True)

    if df.empty:
        hint = " (Try adding '.NS' for Indian stocks, e.g., 'RELIANCE.NS')" if "." not in ticker else ""
        raise ValueError(f"No data found for ticker: {ticker}{hint}")

    if len(df) < 30:
        raise ValueError(f"Insufficient data for {ticker}: only {len(df)} rows found.")

    df.index = pd.to_datetime(df.index)

    current_price = float(df["Close"].iloc[-1])

    # Safer company name extraction
    try:
        info = stock.fast_info
        company_name = getattr(info, "shortName", ticker)
    except Exception:
        company_name = ticker

    return current_price, df, company_name


def get_risk_free_rate(is_indian: bool = False) -> float:
    """
    Fetch risk-free rate.
    US: 10Y Treasury (^TNX)
    India: fallback to RBI repo approx
    """

    if not is_indian:
        try:
            tnx = yf.Ticker("^TNX")
            rate = tnx.history(period="5d")["Close"].iloc[-1] / 100
            return float(rate)
        except Exception:
            pass

    # Fallback (India or failure)
    return 0.065


def get_default_ticker() -> str:
    return "ADANIENT.NS"


if __name__ == "__main__":
    ticker = get_default_ticker()

    price, data, name = fetch_stock_data(ticker)
    rfr = get_risk_free_rate(is_indian=True)

    print(f"\nCompany: {name} ({ticker})")
    print(f"Current Price: ₹{price:.2f}")
    print(f"Risk-Free Rate: {rfr:.2%}")
    print("\nSample Data:")
    print(data.head())