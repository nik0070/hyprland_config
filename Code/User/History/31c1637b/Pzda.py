
def hyprlock_wall_change(hyprlock_conf_path="/home/nik/Documents/hyprlock.conf", wallpaper_path="/home/nik/Pictures/wallpapers/Fantasy-Lake2.png"):
    with open(hyprlock_conf_path) as f:
        lines_list = f.readlines()
        wall_line = lines_list[15]
        wall_line_split = wall_line.split(' ')
        wall_line_split.pop()
        wall_line_split.append(wallpaper_path)    
        print(wall_line_split) 