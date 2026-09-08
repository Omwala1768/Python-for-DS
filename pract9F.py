import pandas as pd

df = pd.read_csv("movies.csv")

df["Rating_Result"] = df["Rating"].apply(
    lambda x: "Highly Rated" if x >= 8.5 else "Average Rated"
)

def calculate_category(rating):
    if rating >= 9.0:
        return "Excellent"
    elif rating >= 8.0:
        return "Very Good"
    elif rating >= 7.0:
        return "Good"
    else:
        return "Average"

df["Rating_Category"] = df["Rating"].apply(calculate_category)

print(df)

print("\nOm Wala S119")
