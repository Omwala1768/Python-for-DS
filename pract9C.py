import pandas as pd

df = pd.read_csv("movies.csv")

print("Title and Rating:")
print(df[["Title", "Rating"]])

print("\nMovies with rating greater than 8.0:")
print(df[df["Rating"] > 8.0])

print("\nMovies released after 2010:")
print(df[df["Release_Year"] > 2010])

print("\nSci-Fi Movies:")
print(df[df["Genre"] == "Sci-Fi"])

print("\nMovies directed by Christopher Nolan:")
print(df[df["Director"] == "Christopher Nolan"])

print("\nMovies with rating greater than 8.0 and duration less than 160 minutes:")
print(df[(df["Rating"] > 8.0) & (df["Duration"] < 160)])

print("\nOm Wala S119")
