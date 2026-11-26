
with open('/proc/stat') as f:
    file = f.read()
    file.readline()

print(file)