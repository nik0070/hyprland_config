import re

#def wlogout_wall_change(wlogout_css_path="/home/nik/Documents/style.css", wallpaper_path="/home/nik/Pictures/wallpapers/Fantasy-Lake2.png"):
    #with open(wlogout_css_path, 'r+') as f:
        #lines_list = f.readlines()
        #wall_line = lines_list[15]
        #print(lines_list)
        #wall_line_split = wall_line.split(" ")
        #wall_line_split.pop()
        #path_text_to_append = wallpaper_path + "\n"
        #wall_line_split.append(path_text_to_append)
        #rec_wall_line = " ".join(wall_line_split)
        #lines_list[15] = rec_wall_line
        #f.seek(0)
        #f.writelines(lines_list)
#

#wlogout_wall_change()


def search_and_replace(search_pattern, replace_sentence, wlogout_css_path="/home/nik/Documents/style.css"):
    search_pattern = r'^background:\s*url\("/home/nik/.+?\.[a-zA-Z0-9]+"\);'
    replace_sentence = "/home/nik/Pictures/wallpapers/changed_wall.png"

    with open(wlogout_css_path, 'r') as f:
        file_contents = f.read()
        print(re.findall(search_pattern)) 

search_and_replace()