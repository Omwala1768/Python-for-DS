import pandas as pd

df = pd.read_csv("movies.csv")

print("Average Rating:", df["Rating"].mean())

print("Maximum Rating:", df["Rating"].max())

print("Minimum Rating:", df["Rating"].min())

print("Median Rating:", df["Rating"].median())

print("Standard Deviation:", df["Rating"].std())

print("Average Duration:", df["Duration"].mean())

print("Number of Movies:", df["Title"].count())

print("Movies with rating above 8.0:",
      (df["Rating"] > 8.0).sum())

print("\nOm Wala S119")
