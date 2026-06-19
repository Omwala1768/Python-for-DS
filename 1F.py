numbers = [12, 45, 7, 23, 89, 34, 56, 10, 67, 122]

print("Original List:", numbers)
maximum = max(numbers)
minimum = min(numbers)
average = sum(numbers) / len(numbers)

print("Maximum:", maximum)
print("Minimum:", minimum)
print("Average:", average)

ascending = sorted(numbers)
descending = sorted(numbers, reverse=True)
print("Ascending Order:", ascending)
print("Descending Order:", descending)

new_number = int(input("Enter a new number to add: "))
numbers.append(new_number)
numbers.pop(0)

print("Updated List:", numbers)
