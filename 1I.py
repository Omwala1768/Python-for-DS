print("Squares of numbers from 1 to 10:")
for i in range(1, 11):
    print(i, "->", i * i)

even_count = 0

print("\nEnter 5 numbers:")
for i in range(5):
    num = int(input("Enter number: "))
    
    if num % 2 == 0:
        even_count += 1

print("\nNumber of even numbers:", even_count)
