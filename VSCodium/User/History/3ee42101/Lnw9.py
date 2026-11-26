
with open('/proc/stat') as f:
    file = f.read()
    file.readlines()

print(file)