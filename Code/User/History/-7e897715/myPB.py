
# def gridtraveller(a, b):
#     if a == 0 or b == 0:
#         return 0 
#     if a == 1 and b == 1:
#         return 1 
#     return gridtraveller(a-1, b) + gridtraveller(a, b-1)

# out = gridtraveller(2, 3)
# print(f'out: {out}')


def gridtraveller(a, b, memo={}):
    key = f'{a},{b}'
    if key in memo.keys():
        return memo[key]
    if a == 0 or b == 0:
        return 0 
    if a == 1 and b == 1:
        return 1 
    memo[key] = gridtraveller(a - 1, b) + gridtraveller(a, b - 1)
    return memo[key]

out = gridtraveller(2,3)
print(out)