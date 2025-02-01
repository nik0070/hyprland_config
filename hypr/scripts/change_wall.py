#!/usr/bin/python

import os
import random
import subprocess
from hyprlock_wall import hyprlock_wall_change
from wlogout_wall import wlogout_wall_change


# Define the directory containing the background images
directory = os.path.expanduser("/home/nik/Pictures/wallpapers/")

images_with_path = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(".jpg") or file.endswith(".png")]

random_background_with_path = random.choice(images_with_path)

# Unload all wallpapers
subprocess.run(["hyprctl", "hyprpaper", "unload", "all"])

# Preload the selected background
subprocess.run(["hyprctl", "hyprpaper", "preload", random_background_with_path])

# Set the wallpaper
subprocess.run(["hyprctl", "hyprpaper", "wallpaper", f",{random_background_with_path}"])


# Changing the Hyprlock wallpaper
hyprlock_wall_change(hyprlock_conf_path="/home/nik/.config/hypr/hyprlock.conf", wallpaper_path=random_background_with_path)


# Changing the wlogout wallpaper
wlogout_wall_change(wlogout_css_path="/home/nik/.config/wlogout/style.css", wallpaper_path=random_background_with_path)

