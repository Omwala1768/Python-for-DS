Tuple1 = ("Om Wala", 122)
Tuple2 = ("Shreyash Kadam", 90)

Nested_Tuple = (Tuple1, Tuple2)
print("Nested Tuple : ", Nested_Tuple)

sorted_tuple = sorted(Nested_Tuple, key=lambda x: x[1])
print("\nSorted Tuple by Roll No : ", sorted_tuple)

copy1 = Nested_Tuple[:]
copy2 = list(Nested_Tuple)
print("\nCopy using slicing:", copy1)
print("Copy using list():", copy2)

try:
    Tuple1[1] = 999
except TypeError as e:
    print("\nTuple is immutable! Error:", e)
