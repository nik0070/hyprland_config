
with open('/proc/stat') as f:
    file = f.readlines()
    agg_cpu_info = file[0]
    split_li = agg_cpu_info.split(' ')[2:]


print(split_li)