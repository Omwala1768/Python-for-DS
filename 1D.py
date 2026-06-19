def original_list(a, i, j):
    a[i], a[j] = a[j], a[i]
    return a

a = ["Apple", "Mango", "Banana", "Strawberry", "Guava", "Chiku"]
print("Original List : ", a)
index1 = 2
index2 = 4

updated_list = original_list(a, index1, index2)
print("Updated List : ", updated_list)
