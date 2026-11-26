-- ============================================================
--  binds.lua
--  Keybindings and program definitions
--  See https://wiki.hypr.land/Configuring/Basics/Binds/
-- ============================================================

-----------------------
---- PROGRAM PATHS ----
-----------------------

local terminal   = "kitty"
local fileManager = "thunar"
local menu       = "wofi --show drun"
local browser    = "zen"
local lockscreen = "hyprlock"
local codeEditor = "code"

local mainMod = "SUPER"


---------------------
---- KEYBINDINGS ----
---------------------

-- Core app launchers
hl.bind(mainMod .. " + return", hl.dsp.exec_cmd(terminal))
hl.bind(mainMod .. " + Q",      hl.dsp.window.close())
hl.bind(mainMod .. " + M",      hl.dsp.exec_cmd("hyprctl dispatch exit"))
hl.bind(mainMod .. " + E",      hl.dsp.exec_cmd(fileManager))
hl.bind(mainMod .. " + V",      hl.dsp.window.float({ action = "toggle" }))
hl.bind(mainMod .. " + A",      hl.dsp.exec_cmd(menu))
hl.bind(mainMod .. " + P",      hl.dsp.window.pseudo())
hl.bind(mainMod .. " + F",      hl.dsp.exec_cmd(browser))
hl.bind(mainMod .. " + L",      hl.dsp.exec_cmd(lockscreen))
hl.bind(mainMod .. " + C",      hl.dsp.exec_cmd(codeEditor))

-- Utility binds
hl.bind(mainMod .. " + R",  hl.dsp.exec_cmd("~/.config/waybar/scripts/relaunch.sh"))
hl.bind(mainMod .. " + W",  hl.dsp.exec_cmd("python ~/.config/hypr/scripts/change_wall.py"))
hl.bind(mainMod .. " + T",  hl.dsp.exec_cmd("pkill -USR1 waybar"))
-- Screenshot: region select → save to ~/Pictures/screenshots/
hl.bind(mainMod .. " + X",  hl.dsp.exec_cmd(
    [[grim -g "$(slurp)" "$HOME/Pictures/screenshots/$(date +'%Y-%m-%d_%H-%M-%S').png"]]
))


-- Focus with arrow keys
hl.bind(mainMod .. " + left",  hl.dsp.focus({ direction = "left"  }))
hl.bind(mainMod .. " + right", hl.dsp.focus({ direction = "right" }))
hl.bind(mainMod .. " + up",    hl.dsp.focus({ direction = "up"    }))
hl.bind(mainMod .. " + down",  hl.dsp.focus({ direction = "down"  }))
hl.bind("ALT + Tab",           hl.dsp.focus({ direction = "down"  }))
hl.bind("ALT + return",        hl.dsp.window.fullscreen())


-- Move window within workspace
-- NOTE: movewindoworgroup moves a window or swaps it out of a group.
-- Verify hl.dsp.window.move_or_group() exists in your Hyprland version;
-- if not, fall back to hl.dsp.window.move({ direction = "..." }).
hl.bind(mainMod .. " + SHIFT + left",  hl.dsp.window.move({ direction = "left"  }))
hl.bind(mainMod .. " + SHIFT + right", hl.dsp.window.move({ direction = "right" }))
hl.bind(mainMod .. " + SHIFT + up",    hl.dsp.window.move({ direction = "up"    }))
hl.bind(mainMod .. " + SHIFT + down",  hl.dsp.window.move({ direction = "down"  }))


-- Switch workspaces 1-10 (0 key maps to workspace 10)
-- Move active window to workspace 1-10
for i = 1, 10 do
    local key = i % 10   -- workspace 10 → key "0"
    hl.bind(mainMod .. " + " .. key,         hl.dsp.focus({ workspace = i }))
    hl.bind(mainMod .. " + SHIFT + " .. key, hl.dsp.window.move({ workspace = i }))
end


-- Special workspace (scratchpad)
hl.bind(mainMod .. " + S",         hl.dsp.workspace.toggle_special("magic"))
hl.bind(mainMod .. " + SHIFT + S", hl.dsp.window.move({ workspace = "special:magic" }))


-- Scroll through workspaces with mainMod + scroll wheel
hl.bind(mainMod .. " + mouse_down", hl.dsp.focus({ workspace = "e+1" }))
hl.bind(mainMod .. " + mouse_up",   hl.dsp.focus({ workspace = "e-1" }))


-- Move / resize windows with mainMod + mouse drag
hl.bind(mainMod .. " + mouse:272", hl.dsp.window.drag(),   { mouse = true })
hl.bind(mainMod .. " + mouse:273", hl.dsp.window.resize(), { mouse = true })


-- Volume (locked + repeating)
hl.bind("XF86AudioRaiseVolume",  hl.dsp.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%+"),    { locked = true, repeating = true })
hl.bind("XF86AudioLowerVolume",  hl.dsp.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-"),    { locked = true, repeating = true })
hl.bind("XF86AudioMute",         hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle"),   { locked = true, repeating = true })
hl.bind("XF86AudioMicMute",      hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle"), { locked = true, repeating = true })

-- Brightness (locked + repeating)
hl.bind("XF86MonBrightnessUp",   hl.dsp.exec_cmd("brightnessctl s 10%+"), { locked = true, repeating = true })
hl.bind("XF86MonBrightnessDown", hl.dsp.exec_cmd("brightnessctl s 10%-"), { locked = true, repeating = true })

-- Media keys (locked)
hl.bind("XF86AudioNext",  hl.dsp.exec_cmd("playerctl next"),        { locked = true })
hl.bind("XF86AudioPause", hl.dsp.exec_cmd("playerctl play-pause"),  { locked = true })
hl.bind("XF86AudioPlay",  hl.dsp.exec_cmd("playerctl play-pause"),  { locked = true })
hl.bind("XF86AudioPrev",  hl.dsp.exec_cmd("playerctl previous"),    { locked = true })
