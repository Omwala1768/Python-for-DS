import math

while True:
    try:
        num = float(input("Enter a number (or type -1 to exit): "))

        if num == -1:
            print("Program Ended.")
            break

        if num < 0:
            print("Square root of a negative number is not possible.")
            continue

        sqrt_value = math.sqrt(num)
        print("Square Root =", sqrt_value)

    except ValueError:
        print("Invalid input! Please enter a valid number.")
