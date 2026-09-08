import pandas as pd

df = pd.read_csv("movies.csv")

print("Original Movie Dataset:")
print(df)

print("\nMissing Values:")
print(df.isnull())

print("\nCount of Missing Values:")
print(df.isnull().sum())

df["Rating"] = df["Rating"].fillna(df["Rating"].mean())

df["Duration"] = df["Duration"].fillna(df["Duration"].mean())

print("\nCleaned Movie Dataset:")
print(df)

print("\nOm Wala S119")
