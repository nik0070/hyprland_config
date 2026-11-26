
with open('/proc/stat') as f:
    file = f.read()

print(file)