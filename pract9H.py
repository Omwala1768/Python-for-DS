import pandas as pd

df = pd.read_csv("movies.csv")

print("Number of Movies in Each Genre:")
print(df.groupby("Genre")["Title"].count())

print("\nAverage Rating by Genre:")
print(df.groupby("Genre")["Rating"].mean())

print("\nMaximum Rating by Genre:")
print(df.groupby("Genre")["Rating"].max())

print("\nAverage Duration by Genre:")
print(df.groupby("Genre")["Duration"].mean())

print("\nOm Wala S119")
