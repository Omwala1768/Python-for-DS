import matplotlib.pyplot as plt

print("Om Wala S119")

subjects = ["Data Structures", "Scala for DS", "Operating System", "Python for DS"]
scores = [65, 70, 74, 60]
explode = [0, 0, 0, 0.2]

plt.pie(scores, labels=subjects, autopct="%1.1f%%", explode=explode)
plt.title("Student Scores")
plt.show()
