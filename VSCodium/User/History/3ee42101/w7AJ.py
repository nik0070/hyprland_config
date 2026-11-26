from functools import reduce

with open('/proc/stat') as f:
    file = f.readlines()
    agg_cpu_info = file[0]
    split_li = agg_cpu_info.split(' ')[2:]
    int_li = [int(num.strip('\n')) for num in split_li]
    idle_time = int_li[3] + int_li[4]
    total_time = reduce(lambda x, y: x + y, int_li)
print(int_li)