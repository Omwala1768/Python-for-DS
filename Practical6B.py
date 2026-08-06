import matplotlib.pyplot as plt

print("Om Wala S119")

x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

plt.plot(x, y, color="red", linestyle="--", marker="o")
plt.title("Customized Line Plot")
plt.xlabel("Numbers")
plt.ylabel("Doubles")
plt.show()
