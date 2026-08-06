import matplotlib.pyplot as plt

print("Om Wala S119")

x = [5, 7, 8, 7, 6, 9, 5]
y = [99, 86, 87, 88, 100, 86, 103]

plt.scatter(x, y, color="green", s=100)
plt.title("Scatter Plot")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()
