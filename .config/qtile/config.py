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

mod = "mod1" # Set mod key
myTerm = "alacritty" # My terminal of choice
myConfig = "/home/lepepe/.config/qtile/config.py" # The Qtile config file location

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
         Key([mod], "Return",
             lazy.spawn(myTerm),
             desc='Launches My Terminal'
             ),
         Key([mod], "d",
             lazy.spawn("rofi -show run"),
             desc='Dmenu Run Launcher'
             ),
         Key([mod], "Tab",
             lazy.next_layout(),
             desc='Toggle through layouts'
             ),
         Key([mod, "shift"], "q",
             lazy.window.kill(),
             desc='Kill active window'
             ),
         Key([mod, "shift"], "r",
             lazy.restart(),
             desc='Restart Qtile'
             ),
         Key([mod, "shift"], "e",
             lazy.shutdown(),
             desc='Shutdown Qtile'
             ),
         ### Treetab controls
         Key([mod, "control"], "k",
             lazy.layout.section_up(),
             desc='Move up a section in treetab'
             ),
         Key([mod, "control"], "j",
             lazy.layout.section_down(),
             desc='Move down a section in treetab'
             ),
         ### Window controls
         Key([mod], "k",
             lazy.layout.down(),
             desc='Move focus down in current stack pane'
             ),
         Key([mod], "j",
             lazy.layout.up(),
             desc='Move focus up in current stack pane'
             ),
         Key([mod, "shift"], "k",
             lazy.layout.shuffle_down(),
             desc='Move windows down in current stack'
             ),
         Key([mod, "shift"], "j",
             lazy.layout.shuffle_up(),
             desc='Move windows up in current stack'
             ),
         Key([mod], "h",
             lazy.layout.grow(),
             lazy.layout.increase_nmaster(),
             desc='Expand window (MonadTall), increase number in master pane (Tile)'
             ),
         Key([mod], "l",
             lazy.layout.shrink(),
             lazy.layout.decrease_nmaster(),
             desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
             ),
         Key([mod], "n",
             lazy.layout.normalize(),
             desc='normalize window size ratios'
             ),
         Key([mod], "m",
             lazy.layout.maximize(),
             desc='toggle window between minimum and maximum sizes'
             ),
         Key([mod, "shift"], "f",
             lazy.window.toggle_floating(),
             desc='toggle floating'
             ),
         Key([mod, "shift"], "m",
             lazy.window.toggle_fullscreen(),
             desc='toggle fullscreen'
             ),
         ### Stack controls
         Key([mod, "shift"], "space",
             lazy.layout.rotate(),
             lazy.layout.flip(),
             desc='Switch which side main pane occupies (XmonadTall)'
             ),
         Key([mod], "space",
             lazy.layout.next(),
             desc='Switch window focus to other pane(s) of stack'
             ),
         Key([mod, "control"], "Return",
             lazy.layout.toggle_split(),
             desc='Toggle between split and unsplit sides of stack'
             ),
         ### My applications launched with SUPER + ALT + KEY
         Key([mod, "mod1"], "n",
             lazy.spawn(myTerm+" -e newsboat"),
             desc='newsboat'
             ),
         Key([mod], "r",
             lazy.spawn(myTerm+" -e rtv"),
             desc='reddit terminal viewer'
             ),
         Key([mod], "e",
             lazy.spawn(myTerm+" -e neomutt"),
             desc='neomutt'
             ),
         Key([mod, "mod1"], "m",
             lazy.spawn(myTerm+" -e sh ./scripts/toot.sh"),
             desc='toot mastodon cli'
             ),
         Key([mod], "f",
             lazy.spawn(myTerm+" -e ranger"),
             desc='vifm'
             ),
         Key([mod], "y",
             lazy.spawn(myTerm+" -e youtube-viewer"),
             desc='youtube-viewer'
             ),
         Key([mod, "mod1"], "a",
             lazy.spawn(myTerm+" -e ncpamixer"),
             desc='ncpamixer'
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
    "border_width": 3,
    "margin": 6,
    "border_focus": kolor01,
    "border_normal": kolor00
}

layouts = [
    #layout.MonadWide(**layout_theme),
    layout.Bsp(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    #layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.VerticalTile(**layout_theme),
    layout.Matrix(**layout_theme),
    #layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Tile(shift_windows=True, **layout_theme),
    layout.Stack(num_stacks=2),
    layout.TreeTab(
         font = "Ubuntu",
         fontsize = 10,
         sections = ["FIRST", "SECOND"],
         section_fontsize = 11,
         bg_color = kolorbg,
         active_bg = kolor04,
         active_fg = kolor12,
         inactive_bg = kolor03,
         inactive_fg = kolorfg,
         padding_y = 5,
         section_top = 10,
         panel_width = 230
    ),
    layout.Floating(**layout_theme)
]

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="Ubuntu Mono",
    fontsize = 12,
    padding = 2,
    background=kolor13
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
              widget.Image(
                       filename = "~/.config/qtile/icons/arch-logo.png",
                       background = kolorbg,
                       margin_x = 5,
                       mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn('rofi -show run'),}
                       ),
              widget.GroupBox(
                       font = "Ubuntu Bold",
                       fontsize = 24,
                       margin_y = 3,
                       margin_x = 0,
                       padding_y = 5,
                       padding_x = 3,
                       borderwidth = 3,
                       active = kolor02,
                       inactive = kolor01,
                       rounded = False,
                       highlight_color = kolorbg,
                       highlight_method = "line",
                       this_current_screen_border = kolor02,
                       this_screen_border = kolor01,
                       other_current_screen_border = kolor00,
                       other_screen_border = kolor00,
                       foreground = kolorfg,
                       background = kolorbg
                       ),
              widget.Prompt(
                       prompt = prompt,
                       font = "Ubuntu Mono",
                       padding = 10,
                       foreground = kolorfg,
                       background = kolorbg
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 20,
                       foreground = kolorfg,
                       background = kolorbg
                       ),
              widget.WindowName(
                       foreground = kolor02,
                       background = kolorbg,
                       padding = 0
                       ),
              widget.StockTicker(
                      foreground = kolorfg,
                      background = kolorbg,
                      padding = 5,
                      apikey="WOQDGOAXJ2URB0OZ",
                      symbol="AAPL"
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
                       fontsize = 14
                       ),
              widget.CheckUpdates(
			distro = "Arch_checkupdates",
			display_format = "{updates}",
			update_interval = 900,
                        foreground = kolorfg,
                        background = kolorbg,
			colour_have_updates = kolor02,
			colour_no_updates = kolorfg
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
                       mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(myTerm + ' -e sudo wifi-menu')},
                       padding = 0,
                       fontsize = 17
                       ),
              widget.Wlan(
                       interface = "wlp3s0",
                       format = '{essid} {quality}/70',
                       foreground = kolorfg,
                       background = kolorbg,
                       padding = 5,
                       mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(myTerm + ' -e sudo wifi-menu')}
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
              widget.Battery(
                       foreground = kolorfg,
                       background = kolorbg,
                       format = '{char} {percent:2.0%} {hour:d}:{min:02d}',
                       update_interval = 5,
                       full_char = "  ",
                       discharge_char = "  ",
                       charge_char = "  "
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
                       foreground = kolorfg,
                       background = kolorbg,
                       format = "%A, %B %d  [ %H:%M ]"
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
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=0.9, size=20)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=20)),
            Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20))]

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
    {'wmclass': 'confirmreset'},
    {'wmclass': 'makebranch'},
    {'wmclass': 'maketag'},
    {'wname': 'branchdialog'},
    {'wname': 'pinentry'},
    {'wmclass': 'ssh-askpass'},
    {'wmclass': 'pavucontrol'},
    {'wmclass': 'slack'},
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
