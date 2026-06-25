numbers = [12, 45, 7, 89, 23, 122, 88, 84, 60]
largest = max(numbers)
print("a. Largest number in the list:", largest)

duplicate_list = [12, 12, 44, 35, 56, 9,9, 24, 6,0,0]
unique_list = list(set(duplicate_list))
print("\nb. List after removing duplicates:", unique_list)

num_list = [10, 15, 20, 25, 30, 35, 40]
even_count = 0

for num in num_list:
    if num % 2 == 0:
        even_count += 1

print("\nc. Number of even elements:", even_count)

user_list = []

print("\nd. Enter 5 numbers:")
for i in range(5):
    num = int(input(f"Enter number {i+1}: "))
    user_list.append(num)

print("List entered by user:", user_list)

def find_average(lst):
    return sum(lst) / len(lst)

average = find_average(user_list)
print("\ne. Average of the numbers:", average)

text = "Practical2"
char_list = list(text)
print("\nf. List of characters:", char_list)

words = ["OM Wala", "MVLU", "Data Science"]
joined_string = " ".join(words)
print("\ng. Joined String:", joined_string)

print("\nProgram made by Om Wala F122!")
