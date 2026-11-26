
with open('/proc/stat') as f:
    file = f.readlines()

print(file)