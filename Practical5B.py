import pandas as pd

print("Om Wala S119")
df = pd.read_csv("fifa.csv")

print("\n========== CSV Data ==========")
print(df)

print("\n========== Statistical Information ==========")
print(df.describe())

print("\n========== Create Series from CSV ==========")
series = pd.Series(df["FRA"])
print(series)

print("\n========== Filter Series with Boolean Array ==========")
filtered = series[series > 10]
print(filtered)
