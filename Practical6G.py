import matplotlib.pyplot as plt
import numpy as np

print("Om Wala S119")

data = np.random.normal(0, 1, 100)

plt.hist(data, bins=20)
plt.title("Histogram")
plt.xlabel("Values")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()
