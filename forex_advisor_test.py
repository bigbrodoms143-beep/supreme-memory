import os, sys, re
import pandas as pd

DATA_FILE = "forex_data.csv"
PAIR = "EUR/USD"

# ========= SELF UPDATE =========
def self_update():
    try:
        filename = __file__
        with open(filename, "r") as f:
            code = f.read()

        # Add safety check if missing
        if "if len(df) < 2:" not in code:
            new_code = re.sub(
                r"latest = df.iloc\[-1\]",
                "if len(df) < 2:\n        return 'NO DATA', 0.0\n    latest = df.iloc[-1]",
                code
            )
            with open(filename, "w") as f:
                f.write(new_code)
            print("✅ Script updated! Restarting...")
            os.execv(sys.executable, ["python"] + sys.argv)
    except Exception as e:
        print(f"⚠️ Update failed: {e}")

self_update()
# ========= END SELF UPDATE =========

def analyze(data, timeframe):
    df = data.resample(timeframe).agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    }).dropna()

    # Safety check
    if len(df) < 2:
        return "NO DATA", 0.0

    latest = df.iloc[-1]
    prev = df.iloc[-2]

    if latest["Close"] > prev["Close"]:
        signal = "BUY"
    elif latest["Close"] < prev["Close"]:
        signal = "SELL"
    else:
        signal = "HOLD"

    return signal, latest["Close"]

def main():
    print("📊 Forex Advisor (Test with Self-Update)")
    data = pd.read_csv(DATA_FILE, parse_dates=["Date"], index_col="Date")

    timeframes = {
        "15m": "15min",
        "30m": "30min",
        "1h": "1h",
        "2h": "2h",
        "4h": "4h",
        "1D": "1d"
    }

    overall = []
    for label, tf in timeframes.items():
        signal, price = analyze(data, tf)
        print(f"⏱ {label} | Price: {price:.5f} | Advice: {signal}")
        overall.append(signal)

    # Simple consensus
    from collections import Counter
    trend = Counter(overall).most_common(1)[0][0]
    print(f"\n📌 Overall Trend: {trend}")
    print("✅ Test analysis complete.")

if __name__ == "__main__":
    main()
