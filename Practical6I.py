import matplotlib.pyplot as plt
import numpy as np

print("Om Wala S119")

x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

subjects = ["DS", "Scala", "OS", "Python"]
scores = [65, 70, 74, 60]

sx = [5, 7, 8, 7, 6, 9, 5]
sy = [99, 86, 87, 88, 100, 86, 103]

data = np.random.normal(0, 1, 100)

plt.figure(figsize=(10, 8))

plt.subplot(2, 2, 1)
plt.plot(x, y)
plt.title("Line Plot")

plt.subplot(2, 2, 2)
plt.bar(subjects, scores)
plt.title("Bar Chart")

plt.subplot(2, 2, 3)
plt.scatter(sx, sy)
plt.title("Scatter Plot")

plt.subplot(2, 2, 4)
plt.hist(data, bins=20)
plt.title("Histogram")

plt.tight_layout()
plt.show()
