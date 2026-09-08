import pandas as pd

df = pd.read_csv("movies.csv")

print("Movie Dataset:")
print(df)

print("\nFirst 10 Movie Records:")
print(df.head(10))

print("\nNumber of Movies:")
print(len(df))

print("\nColumn Names:")
print(df.columns)

print("\nAverage Movie Rating:")
print(df["Rating"].mean())

print("\nAverage Movie Duration:")
print(df["Duration"].mean())

print("\nOm Wala S119")
