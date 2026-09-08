import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("movies.csv")

plt.figure(figsize=(10, 5))
plt.bar(df["Title"], df["Rating"])
plt.xlabel("Movie Title")
plt.ylabel("Rating")
plt.title("Movie Ratings")
plt.xticks(rotation=45)

plt.figure(figsize=(10, 5))
plt.plot(df["Title"], df["Rating"], marker="o")
plt.xlabel("Movie Title")
plt.ylabel("Rating")
plt.title("Movie Ratings - Line Chart")
plt.xticks(rotation=45)

plt.figure(figsize=(8, 5))
plt.hist(df["Rating"], bins=5)
plt.xlabel("Rating")
plt.ylabel("Number of Movies")
plt.title("Distribution of Movie Ratings")

genre_count = df["Genre"].value_counts()

plt.figure(figsize=(7, 7))
plt.pie(genre_count, labels=genre_count.index,
        autopct="%1.1f%%")
plt.title("Movies by Genre")

plt.show()

print("Om Wala S119")
