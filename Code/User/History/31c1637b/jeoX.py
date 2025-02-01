
with open("/home/nik/Documents/hyprlock.conf") as f:
    lines_list = f.readlines()
    wall_line = lines_list[15]
    wall_line_split = wall_line.split(' ')
    
    print(wall_line_split) 