import numpy as np

arr = np.array([12, 122, 119, 91, 85, 108, 85])

max_value = np.max(arr)
filter_array = arr[arr == max_value]

print("Om Wala S119")
print("Max Value from Array : " , max_value)
print("Filter Array : " , filter_array)
