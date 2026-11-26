
def combine(n: int, k: int) -> list[list[int]]:
    nums = list(range(1, n + 1))
    result = []
    def backtrack(i, subset):
        # Base
        if i == n or len(subset) == k:
            result.append(subset.copy())
            return

        subset.append(nums[i])
        backtrack(i + 1, subset)

        subset.pop()
        backtrack(i + 1, subset)

    backtrack(0, [])
    return result
    
out = combine(4, 2)
print(out)