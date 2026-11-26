
def combine(n: int, k: int) -> list[list[int]]:
    nums = list(range(1, n + 1))
    result = []
    def backtrack(i, subset):
        # Base
        if len(subset) == k:
            result.append(subset.copy())
            return
        elif len(subset) == k and i == n:
            result.append(subset.copy())
            return 
        else:
            return

        subset.append(nums[i])
        backtrack(i + 1, subset)

        subset.pop()
        backtrack(i + 1, subset)

    backtrack(0, [])
    return result
    
out = combine(4, 2)
print(out)