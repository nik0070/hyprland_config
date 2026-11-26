
def topKFrequent(nums: list[int], K:int) -> list[int]:
    freq_map = {}
    for num in nums:
        if num in freq_map.keys():
            freq_map[num] += 1
        else:
            freq_map[num] = 1
    return freq_map

out = topKFrequent([1, 1, 1, 1, 2, 2, 2, 3], 2)
print(out)
