import pandas as pd

df = pd.read_csv("movies.csv")

print("Rating in Ascending Order:")
print(df.sort_values("Rating"))

print("\nRating in Descending Order:")
print(df.sort_values("Rating", ascending=False))

print("\nDuration in Descending Order:")
print(df.sort_values("Duration", ascending=False))

print("\nTop 5 Movies:")
print(df.sort_values("Rating", ascending=False).head(5))

print("\nBottom 3 Movies:")
print(df.sort_values("Rating").head(3))

print("\nOm Wala S119")
