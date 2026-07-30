import pandas as pd

print("Om Wala S119")

print("\n========== 5a. Create DataFrame ==========")

data = {
    "Movie": ["Inception", "Interstellar", "Avengers", "Joker"],
    "Rating": [8.8, 8.7, 8.4, 8.5]
}

df = pd.DataFrame(data)

print(df)


print("\n========== 5b. Statistical Information ==========")

print(df.describe())


print("\n========== 5c. Create Pandas Series from Dictionary ==========")

movie_ratings = {
    "Inception": 8.8,
    "Interstellar": 8.7,
    "Avengers": 8.4,
    "Joker": 8.5
}

series = pd.Series(movie_ratings)

print(series)


print("\n========== 5d. Filter Pandas Series with Boolean Array ==========")

filtered = series[series > 8.5]

print(filtered)
