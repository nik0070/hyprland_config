import heapq

def topKFrequent(nums: list[int], K:int) -> list[int]:
    freq_map = {}
    for num in nums:
        if num in freq_map.keys():
            freq_map[num] += 1
        else:
            freq_map[num] = 1

    lt = list(freq_map.items())
    rev_lt = [(freq, num) for (num, freq) in lt]
    heap = []
    for tup in rev_lt:
        heapq.heappush(heap, tup)
        if len(heap) > K:
            heapq.heappop(heap)
    result = [num for freq, num in heap]
    return result

out = topKFrequent([1, 1, 1, 1, 2, 2, 2, 3], 2)
print(out)
