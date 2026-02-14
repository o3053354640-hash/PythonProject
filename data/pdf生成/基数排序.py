def radix_sort(arr):
    if not arr:
        return arr

    # 找到最大值，确定需要多少位（d）
    max_num = max(arr)

    # 从个位开始，对每一位进行计数排序
    exp = 1  # 当前位：1（个位）、10（十位）、100（百位）...
    while max_num // exp > 0:
        counting_sort_by_digit(arr, exp)
        exp *= 10


def counting_sort_by_digit(arr, exp):
    """
    根据指定的位（exp 表示 1, 10, 100...）对数组进行稳定排序
    使用计数排序作为子过程
    """
    n = len(arr)
    output = [0] * n  # 输出数组
    count = [0] * 10  # 十进制：0~9 共10个桶

    # 统计当前位上每个数字（0-9）出现的次数
    for num in arr:
        digit = (num // exp) % 10
        count[digit] += 1

    # 将 count 转换为累积计数（确定每个数字在 output 中的位置）
    for i in range(1, 10):
        count[i] += count[i - 1]

    # 从后往前遍历原数组（保证稳定性），构建 output
    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1

    # 将排序结果复制回原数组
    for i in range(n):
        arr[i] = output[i]


nums = [170, 45, 75, 90, 2, 802, 24, 66]
print("排序前:", nums)
radix_sort(nums)
print("排序后:", nums)