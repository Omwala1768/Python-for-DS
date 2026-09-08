import pandas as pd

print("Om Wala S119")

data = {
    "Student_ID": [101, 102, 103, 104, 105, 106, 107, 108],
    "Name": ["Om", "Shreyash", "Krish", "Deepak", "Palak", "Sahil", "Vedant", "Krishna"],
    "Age": [19, 20, 19, 21, 20, 19, 21, 20],
    "Gender": ["Male", "Male", "Male", "Female",
               "Female", "Male", "Male", "Male"],
    "Course": ["BSc CS", "BSc CS", "BSc IT", "BSc CS",
               "BSc IT", "BSc CS", "BSc IT", "BSc CS"],
    "Marks": [98, 93, 67, 92, 88, 74, 81, 69]
}

df = pd.DataFrame(data)
print("Complete Dataset:")
print(df)
print("\nFirst 5 Records:")
print(df.head())
print("\nLast 5 Records:")
print(df.tail())
print("\nShape:")
print(df.shape)
print("\nColumn Names:")
print(df.columns)
print("\nDataset Information:")
df.info()
print("\nStatistical Information:")
print(df.describe())
