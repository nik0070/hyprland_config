
def subsets(nums: list[int]) -> list[list[int]]:
    sub_li = []
    def backtrack(i, subset):
        if i == len(nums):
            sub_li.append(subset.copy())

        subset.append(i)
        subset = backtrack(i+1, subset)
        subset.pop()

        