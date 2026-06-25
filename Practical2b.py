my_tuple = ("Om Wala", 122, 5.10, "MVLU", "Python for DS")
print("a. Tuple:", my_tuple)

print("\nb. First element:", my_tuple[0])
print("Last element:", my_tuple[-1])

print("\nc. Middle 3 elements:", my_tuple[1:4])

tuple1 = (122, 90, 88)
tuple2 = (84, 129, 127)
concat_tuple = tuple1 + tuple2
print("\nd. Concatenated Tuple:", concat_tuple)

reversed_tuple = my_tuple[::-1]
print("\ne. Reversed Tuple:", reversed_tuple)

count_tuple = ("om", "shreyash", "om", "palak", "krish", "deepak", "om")
count = count_tuple.count("om")
print("\nf. 'om' appears", count, "times")

index = my_tuple.index(122)
print("\ng. Index of 122:", index)

element = 122
print("\nh. Checking if", element, "exists in tuple ?")
if element in my_tuple:
    print("Element exists.")
else:
    print("Element does not exist.")

my_list = [100, 200, 300, 400, 500]
converted_tuple = tuple(my_list)
print("\ni. Converted Tuple:", converted_tuple)

unsorted_tuple = (59, 11, 43, 20, 30, 122, 88, 90, 84)
sorted_tuple = tuple(sorted(unsorted_tuple))
print("\nj. Sorted Tuple:", sorted_tuple)

repeat_tuple = (1, 2, 3)
repeated = repeat_tuple * 3
print("\nk. Repeated Tuple:", repeated)

print("\nl. Checking tuple immutability")
try:
    my_tuple[0] = 100
except TypeError as e:
    print("Error:", e)

print("Tuples are immutable and cannot be modified.")

print("\nProgram made by Om Wala F122!")
