
with open("/home/nik/Documents/hyprlock.conf") as f:
    lines_list = f.readlines()
    req_line = lines_list[15]

    print(req_line) 