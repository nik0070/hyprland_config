from functools import reduce
import time

with open('/proc/stat') as f:
    file = f.readlines()
    agg_cpu_info = file[0]
    split_li = agg_cpu_info.split(' ')[2:]
    int_li = [int(num.strip('\n')) for num in split_li]
    idle_time = int_li[3] + int_li[4]
    total_time = reduce(lambda x, y: x + y, int_li)
    
time.sleep(1)

with open('/proc/stat') as f:
    file = f.readlines()
    agg_cpu_info = file[0]
    split_li = agg_cpu_info.split(' ')[2:]
    int_li = [int(num.strip('\n')) for num in split_li]
    n_idle_time = int_li[3] + int_li[4]
    n_total_time = reduce(lambda x, y: x + y, int_li)

delta_total = n_total_time - total_time
delta_idle = n_idle_time - idle_time

cpu_per = ((delta_total - delta_idle)/delta_total) * 100

output_text = f"CPU Usage: {cpu_per}%"
print(output_text)