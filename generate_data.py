import pandas as pd
import numpy as np

np.random.seed(42)

rows = 10000

price = np.cumsum(np.random.randn(rows)) + 100

df = pd.DataFrame({
    "open": price + np.random.randn(rows),
    "high": price + np.random.rand(rows)*2,
    "low": price - np.random.rand(rows)*2,
    "close": price,
    "volume": np.random.randint(100, 1000, rows)
})

df.to_csv("data.csv", index=False)

print("Correct OHLCV data.csv generated!")