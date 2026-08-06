import matplotlib.pyplot as plt

print("Om Wala S119")

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
sales_2023 = [150, 200, 250, 300, 280, 350]
sales_2024 = [180, 220, 270, 320, 300, 400]

plt.plot(months, sales_2023, color="blue", linestyle="--", marker="o", label="2023")
plt.plot(months, sales_2024, color="green", linestyle="-", marker="s", label="2024")

max_sales = max(sales_2024)
max_index = sales_2024.index(max_sales)

plt.annotate(
    "Highest Sales",
    xy=(months[max_index], max_sales),
    xytext=(months[max_index], max_sales + 20),
    arrowprops=dict(arrowstyle="->")
)

plt.title("Monthly Sales Comparison (2023 vs 2024)")
plt.xlabel("Months")
plt.ylabel("Sales")
plt.legend()

plt.savefig("sales_comparison.png")

plt.show()
