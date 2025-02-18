def cansum(num, lst):
    # Base cases
    if num < 0:
        return False
    elif num == 0:
        return True
    
    for i in lst:
        return cansum(num - i, lst)

cansum(7, [5, 3, 4, 7])