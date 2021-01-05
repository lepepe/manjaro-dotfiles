# -*- coding: utf-8 -*-
import os
import re
import socket
import subprocess
from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from typing import List  # noqa: F401
import json

mod = "mod1"                                        # Sets mod key to Alt
myTerm = "alacritty"                                # My terminal of choice
myConfig = "/home/lepepe/.config/qtile/config.py"   # The Qtile config file location

# pull pywal colors from cached template
pykolors = os.path.expanduser('~/.cache/wal/colors.json')

# parse pywal json file into python format
kolors = json.loads(open(pykolors).read())

# list of colors from json file - to be placed in qtile
kolorbg = kolors['special']['background']
kolorfg = kolors['special']['foreground']
kolorcs = kolors['special']['cursor']
kolor00 = kolors['colors']['color0']
kolor01 = kolors['colors']['color1']
kolor02 = kolors['colors']['color2']
kolor03 = kolors['colors']['color3']
kolor04 = kolors['colors']['color4']
kolor05 = kolors['colors']['color5']
kolor06 = kolors['colors']['color6']
kolor07 = kolors['colors']['color7']
kolor08 = kolors['colors']['color8']
kolor09 = kolors['colors']['color9']
kolor10 = kolors['colors']['color10']
kolor11 = kolors['colors']['color11']
kolor12 = kolors['colors']['color12']
kolor13 = kolors['colors']['color13']
kolor14 = kolors['colors']['color14']
kolor15 = kolors['colors']['color15']

keys = [
    ### The essentials
    Key(
        [mod], "Return",
        lazy.spawn(myTerm),
        desc='Launches Terminal'
    ),
    Key(
        [mod], "d",
        lazy.spawn("rofi -show run"),
        desc='Rofi Application Launcher'
    ),
    Key(
        [mod], "Tab",
        lazy.next_layout(),
        desc='Toggle through layouts'
    ),
    Key(
        [mod, "shift"], "q",
        lazy.window.kill(),
        desc='Kill active window'
    ),
    Key(
        [mod, "shift"], "r",
        lazy.restart(),
        desc='Restart Qtile'
    ),
    Key(
        [mod, "shift"], "e",
        lazy.shutdown(),
        desc='Shutdown Qtile'
    ),
    ### Window controls
    Key(
        [mod], "k",
        lazy.layout.down(),
        desc='Move focus down in current stack pane'
    ),
    Key(
        [mod], "j",
        lazy.layout.up(),
        desc='Move focus up in current stack pane'
    ),
    Key(
        [mod, "shift"], "k",
        lazy.layout.shuffle_down(),
        desc='Move windows down in current stack'
    ),
    Key(
        [mod, "shift"], "j",
        lazy.layout.shuffle_up(),
        desc='Move windows up in current stack'
    ),
    Key(
        [mod], "h",
        lazy.layout.grow(),
        lazy.layout.increase_nmaster(),
        desc='Expand window (MonadTall), increase number in master pane (Tile)'
    ),
    Key(
        [mod], "l",
        lazy.layout.shrink(),
        lazy.layout.decrease_nmaster(),
        desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
    ),
    Key(
        [mod], "n",
        lazy.layout.normalize(),
        desc='normalize window size ratios'
    ),
    Key(
        [mod], "m",
        lazy.layout.maximize(),
        desc='toggle window between minimum and maximum sizes'
    ),
    Key(
        [mod, "shift"], "f",
        lazy.window.toggle_floating(),
        desc='toggle floating'
    ),
    Key(
        [mod, "shift"], "m",
        lazy.window.toggle_fullscreen(),
        desc='toggle fullscreen'
    ),
    ### Stack controls
    Key(
        [mod, "shift"], "space",
        lazy.layout.rotate(),
        lazy.layout.flip(),
        desc='Switch which side main pane occupies (XmonadTall)'
    ),
    Key(
        [mod], "space",
        lazy.layout.next(),
        desc='Switch window focus to other pane(s) of stack'
    ),
    Key(
        [mod, "control"], "Return",
        lazy.layout.toggle_split(),
        desc='Toggle between split and unsplit sides of stack'
    ),
    ### Dmenu scripts launched with ALT + CTRL + KEY
    Key(
        ["mod1", "control"], "e",
        lazy.spawn("./.dmenu/dmenu-edit-configs.sh"),
        desc='Dmenu script for editing config files'
    ),
    ### My applications launched with ALT + SHIFT
    Key(
        [mod, "shift"], "b",
        lazy.spawn("qutebrowser"),
        desc='Launches Qutebrowser'
    ),
    Key(
        [mod, "mod1"], "e",
        lazy.spawn(myTerm+" -e neomutt"),
        desc='neomutt'
    ),
    Key(
        [mod, "mod1"], "t",
        lazy.spawn(myTerm+" -e sh ./scripts/tig-script.sh"),
        desc='tig'
    ),
    Key(
        [mod, "shift"], "s",
        lazy.spawn(myTerm+" -e sncli"),
        desc='SimpleNote CLI'
    ),
    Key(
        [mod, "shift"], "y",
        lazy.spawn(myTerm+" -e youtube-viewer"),
        desc='youtube-viewer'
    ),
]

group_names = [
    ("", {'layout': 'monadtall'}),
    ("", {'layout': 'monadtall'}),
    ("", {'layout': 'floating'}),
    ("", {'layout': 'monadtall'}),
    ("", {'layout': 'monadtall'}),
    ("", {'layout': 'floating'})
]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group

layout_theme = {
    "border_width": 2,
    "margin": 6,
    "border_focus": kolor01,
    "border_normal": kolor00
}

layouts = [
    layout.Bsp(**layout_theme),
    layout.Matrix(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Tile(shift_windows=True, **layout_theme),
    layout.Stack(num_stacks=2),
    layout.Floating(**layout_theme)
]

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="DejaVu Sans Mono",
    fontsize = 12,
    padding = 2,
    background=kolor02
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
        widget.Sep(
           linewidth = 0,
           padding = 6,
           foreground = kolorfg,
           background = kolorbg
        ),
        widget.TextBox(
           font = 'Font Awesome 5 Free',
           text = "",
           padding = 10,
           foreground = kolor05,
           background = kolorbg,
           fontsize = 20,
           mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn('rofi -show run')}
        ),
        widget.GroupBox(
           font = "DejaVu Sans Mono",
           fontsize = 20,
           margin_y = 3,
           margin_x = 3,
           padding_y = 5,
           padding_x = 3,
           borderwidth = 3,
           active = kolor05,
           inactive = kolor05,
           rounded = False,
           highlight_color = kolorbg,
           highlight_method = "line",
           this_current_screen_border = kolor05,
           this_screen_border = kolor04,
           other_current_screen_border = kolor00,
           other_screen_border = kolor00,
           foreground = kolor02,
           background = kolor00
        ),
        widget.Prompt(
           prompt = prompt,
           font = "DejaVu Sans Mono",
           padding = 0,
           foreground = kolorfg,
           background = kolorbg
        ),
        widget.Sep(
           linewidth = 0,
           padding = 20,
           foreground = kolor02,
           background = kolor00
        ),
        widget.WindowName(
           foreground = kolor05,
           background = kolor00,
           padding = 0
        ),
        widget.TextBox(
           text = " ₿",
           padding = 0,
           foreground = kolorfg,
           background = kolorbg,
           fontsize = 12
        ),
        widget.BitcoinTicker(
           foreground = kolorfg,
           background = kolorbg,
           padding = 5
        ),
        widget.TextBox(
           text = " ",
           padding = 2,
           foreground = kolorfg,
           background = kolorbg,
           fontsize = 17
        ),
        widget.ThermalSensor(
           foreground = kolorfg,
           background = kolorbg,
           threshold = 90,
           padding = 5
        ),
        widget.TextBox(
           text = " ⟳",
           padding = 2,
           foreground = kolorfg,
           background = kolorbg,
           fontsize = 17
        ),
        widget.CheckUpdates(
           distro = "Arch",
           display_format = "{updates}",
           update_interval = 900,
           colour_have_updates = kolorfg,
           colour_no_updates = kolorfg,
           foreground = kolorfg,
           background = kolorbg
        ),
        widget.TextBox(
           text = "Updates",
           padding = 5,
           mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syu')},
           foreground = kolorfg,
           background = kolorbg
        ),
        widget.TextBox(
           text = "  ",
           foreground = kolorfg,
           background = kolorbg,
           padding = 0,
           fontsize = 17
        ),
        widget.Memory(
           foreground = kolorfg,
           background = kolorbg,
           mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(myTerm + ' -e htop')},
           padding = 5
        ),
        widget.TextBox(
           text = " ",
           foreground = kolorfg,
           background = kolorbg,
           padding = 0,
           fontsize = 17
        ),
        widget.Wlan(
           interface = "wlp0s20f3",
           format = '{essid} {quality}/70',
           foreground = kolorfg,
           background = kolorbg,
           padding = 5,
           mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(myTerm + ' -e nmcli device wifi list')}
        ),
        widget.TextBox(
          text = " Vol:",
           foreground = kolorfg,
           background = kolorbg,
          padding = 0
        ),
        widget.Volume(
           foreground = kolorfg,
           background = kolorbg,
           padding = 5
        ),
        widget.CurrentLayoutIcon(
           custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
           foreground = kolorfg,
           background = kolorbg,
           padding = 0,
           scale = 0.7
        ),
        widget.CurrentLayout(
           foreground = kolorfg,
           background = kolorbg,
           padding = 5
        ),
        widget.Clock(
           foreground = kolor01,
           background = kolorbg,
           format = "%B %d - %H:%M"
        ),
        widget.Sep(
           linewidth = 0,
           padding = 10,
           foreground = kolorfg,
           background = kolorbg,
        ),
        widget.Systray(
           background = kolor00,
           padding = 5
        ),
    ]
    return widgets_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1                       # Slicing removes unwanted widgets on Monitors 1,3

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2                       # Monitor 2 will display all widgets in widgets_list

def init_screens():
    return [
        Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20)),
        Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=20)),
        Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20))
    ]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wname': 'pinentry'},
    {'wname': 'sncli'},
    {'wmclass': 'Pavucontrol'},
    {'wmclass': 'zoom'},
    {'wmclass': 'Signal'},
    {'wmclass': 'Simplenote'},
    {'wmclass': 'Lxappearance'},
    {'wmclass': 'Bitwarden'},
])
auto_fullscreen = True
focus_on_window_activation = "smart"

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

