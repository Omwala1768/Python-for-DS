students = {"Om": 99,"Shreyash": 98,"Deepak": 82,"Krish": 78,"Tanmay": 61}

print("Student Names and Marks:")
for name, marks in students.items():
    print(name, ":", marks)

average = sum(students.values()) / len(students)
print("\nClass Average:", average)

top_student = max(students, key=students.get)
print("Student with Highest Marks:", top_student)
print("Highest Marks:", students[top_student])
