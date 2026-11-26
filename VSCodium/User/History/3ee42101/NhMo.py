
with open('/proc/stat') as f:
    file = f.readlines()
    agg_cpu_info = file[0]

print(agg_cpu_info)