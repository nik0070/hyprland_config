def cansum(num, lst):
    # Base cases
    if num == 0:
        return True
    
    for i in lst:
        print(i)
        next_num = num - i
        if next_num < 0:
            continue
        return cansum(num - i, lst)
    return False

out = cansum(7, [5, 3, 4, 7])
print(out)