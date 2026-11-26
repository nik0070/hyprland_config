import heapq

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

lt = list(out.items())
print(lt)
rev_lt = [(freq, num) for (num, freq) in lt]
print(rev_lt)

heap = []
k = 2

for tup in rev_lt:
    heapq.heappush(heap, tup)
    if len(heap) > k:
        heapq.heappop(heap)

print(heap)

