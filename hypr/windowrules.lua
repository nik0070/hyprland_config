-- ============================================================
--  windowrules.lua
--  Window rules and workspace rules
--  See https://wiki.hypr.land/Configuring/Basics/Window-Rules/
-- ============================================================

-- Suppress maximize requests from all apps
hl.window_rule({
    name  = "suppress-maximize-events",
    match = { class = ".*" },
    suppress_event = "maximize",
})

-- Fix some dragging issues with XWayland
hl.window_rule({
    name  = "fix-xwayland-drags",
    match = {
        class      = "^$",
        title      = "^$",
        xwayland   = true,
        float      = true,
        fullscreen = false,
        pin        = false,
    },
    no_focus = true,
})

-- Opacity rules: active 0.96, inactive 0.85
-- These mirror: windowrule = opacity 0.96 override 0.85 override, match:class <app>
hl.window_rule({
    name  = "opacity-thunar",
    match = { class = "thunar" },
    opacity = "0.96 override 0.85 override",
})

hl.window_rule({
    name  = "opacity-firefox",
    match = { class = "firefox" },
    opacity = "0.96 override 0.85 override",
})

hl.window_rule({
    name  = "opacity-zen",
    match = { class = "zen" },
    opacity = "0.96 override 0.85 override",
})

hl.window_rule({
    name  = "opacity-code",
    match = { class = "codium" },
    opacity = "0.96 override 0.85 override",
})

hl.window_rule({
    name  = "opacity-Antigravity",
    match = { class = "antigravity" },
    opacity = "0.96 override 0.85 override",
})

-- Hyprland-run float rule
hl.window_rule({
    name  = "move-hyprland-run",
    match = { class = "hyprland-run" },
    move  = "20 monitor_h-120",
    float = true,
})

-- Uncomment for "smart gaps" (no gaps when only one window):
-- hl.workspace_rule({ workspace = "w[tv1]", gaps_out = 0, gaps_in = 0 })
-- hl.workspace_rule({ workspace = "f[1]",   gaps_out = 0, gaps_in = 0 })
-- hl.window_rule({ name = "no-gaps-wtv1", match = { float = false, workspace = "w[tv1]" }, border_size = 0, rounding = 0 })
-- hl.window_rule({ name = "no-gaps-f1",   match = { float = false, workspace = "f[1]"   }, border_size = 0, rounding = 0 })
