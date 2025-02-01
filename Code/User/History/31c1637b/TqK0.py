
def hyprlock_wall_change(hyprlock_conf_path="/home/nik/Documents/hyprlock.conf", wallpaper_path="/home/nik/Pictures/wallpapers/Fantasy-Lake2.png"):
    with open(hyprlock_conf_path, 'r+') as f:
        lines_list = f.readlines()
        
        wall_line = lines_list[15]
        wall_line_split = wall_line.split(" ")
        wall_line_split.pop()
        path_text_to_append = wallpaper_path + "\n"
        wall_line_split.append(path_text_to_append)
        rec_wall_line = " ".join(wall_line_split)
        lines_list[15] = rec_wall_line
        f.seek(0)
        f.truncate()
        f.writelines(lines_list)

if __name__ == '__main__':
    hyprlock_wall_change()