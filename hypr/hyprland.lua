-- ============================================================
--  Hyprland Lua Config  (converted from hyprlang)
--  https://wiki.hypr.land/Configuring/Start/
--
--  Structure:
--    hyprland.lua     ← this file (monitors, env, look & feel, input)
--    animations.lua   ← curves + animations
--    binds.lua        ← keybindings & programs
--    windowrules.lua  ← window / layer rules
-- ============================================================

require("animations")
require("binds")
require("windowrules")


------------------
---- MONITORS ----
------------------

-- See https://wiki.hypr.land/Configuring/Basics/Monitors/
hl.monitor({
    output   = "eDP-1",
    mode     = "2560x1440@165",
    position = "auto",
    scale    = 1,
})

hl.monitor({
    output   = "HDMI-A-1",
    mode     = "1920x1080@74.99",
    position = "auto",
    scale    = 1,
})


-------------------
---- AUTOSTART ----
-------------------

-- See https://wiki.hypr.land/Configuring/Basics/Autostart/
hl.on("hyprland.start", function()
    hl.exec_cmd("nm-applet")
    hl.exec_cmd("waybar")
    hl.exec_cmd("hyprpaper")
end)


-------------------------------
---- ENVIRONMENT VARIABLES ----
-------------------------------

-- See https://wiki.hypr.land/Configuring/Advanced-and-Cool/Environment-variables/
hl.env("XCURSOR_SIZE",              "24")
hl.env("HYPRCURSOR_SIZE",           "24")
hl.env("LIBVA_DRIVER_NAME",         "nvidia")
hl.env("__GLX_VENDOR_LIBRARY_NAME", "nvidia")
hl.env("AQ_DRM_DEVICES",            "/dev/dri/card1:/dev/dri/card0")


-----------------------
---- LOOK AND FEEL ----
-----------------------

-- See https://wiki.hypr.land/Configuring/Basics/Variables/
hl.config({
    general = {
        gaps_in  = 4,
        gaps_out = 4,

        border_size = 0,

        col = {
            active_border   = { colors = { "rgba(33ccffee)", "rgba(00ff99ee)" }, angle = 45 },
            inactive_border = "rgba(595959aa)",
        },

        resize_on_border = false,
        allow_tearing    = false,
        layout           = "dwindle",
    },

    decoration = {
        rounding = 6,

        shadow = {
            enabled      = true,
            range        = 10,
            render_power = 3,
--          color        = "rgba(1a1a1aee)",
	    color        = "rgba(0,0,0,0.6)",
	    color_inactive = "rgba(0,0,0,0.3)",
        },

        -- blur is intentionally disabled (commented in original)
        -- blur = {
        --     enabled  = true,
        --     size     = 1,
        --     passes   = 1,
        --     vibrancy = 0.1696,
        -- },
    },

    animations = {
        enabled = true,
    },
})

-- See https://wiki.hypr.land/Configuring/Layouts/Dwindle-Layout/
hl.config({
    dwindle = {
        preserve_split = true,
    },
})

-- See https://wiki.hypr.land/Configuring/Layouts/Master-Layout/
hl.config({
    master = {
        new_status = "master",
    },
})

hl.config({
    misc = {
        force_default_wallpaper = 0,     -- 0 disables anime mascot wallpapers
        disable_hyprland_logo   = false,
    },
})


---------------
---- INPUT ----
---------------

hl.config({
    input = {
        kb_layout  = "us",
        kb_variant = "",
        kb_model   = "",
        kb_options = "",
        kb_rules   = "",

        follow_mouse = 1,
        sensitivity  = 0,   -- -1.0 to 1.0, 0 = no modification

        touchpad = {
            natural_scroll = true,
            scroll_factor  = 0.5,
        },
    },
})

-- Per-device config — see https://wiki.hypr.land/Configuring/Advanced-and-Cool/Devices/
hl.device({
    name        = "epic-mouse-v1",
    sensitivity = -0.5,
})
