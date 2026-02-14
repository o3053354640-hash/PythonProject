def bubbleSort(numbers):
    n = len(numbers)
    for j in range(n - 1):  # 外层循环：最多需要 n-1 趟
        for i in range(n - 1 - j):  # 内层循环：每趟比较到未排序部分的末尾
            if numbers[i] > numbers[i + 1]:
                numbers[i], numbers[i + 1] = numbers[i + 1], numbers[i]

arr = [64, 34, 25, 12, 22, 11, 90]
bubbleSort(arr)
print(arr)  
