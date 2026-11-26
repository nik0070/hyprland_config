
with open('/proc/stat') as f:
    file = f.readlines()
    agg_cpu_info = file[0]
    split_li = agg_cpu_info.split(' ')


print(split_li)