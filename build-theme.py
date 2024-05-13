#!/usr/bin/env python3

import json
import argparse
import sys
import os


#############
# functions #
#############

def data_sub_link(dictio, key, value):
    """
    return type: void
    description:
      replace the "@key_name" links
      with the color string value of
      the refferenced key
    """
    if value.find("@") > -1:
        index_str = value[1:]
        dictio[key] = dictio[index_str]
        if args.debug:
            print("{k}: {v}".format(k=key, v=dictio[key]))


def data_rgb_to_hex(dictio, key, value):
    """
    return type: void
    description:
      replace the "rgba()" values
      with the correspinding rgb hex string
    """
    if value.find("rgb") > -1:
        oparen = value.find("(")
        cparen = value.find(")")
        # index_str = value[1:]
        vallist = value[oparen+1:cparen].split(",")
        r = int(vallist[0])
        g = int(vallist[1])
        b = int(vallist[2])
        res = "#{0:02x}{1:02x}{2:02x}".format(r, g, b)
        dictio[key] = res
        if args.debug:
            print("{k}: {v}".format(
                k=key, v=dictio[key]))


def hex_to_rgb(color):
    """Convert a hex color to rgb."""
    tup = tuple(bytes.fromhex(color.strip("#")))
    return "%d, %d, %d" % (*tup,)


########
# Main #
########

# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-f", "--file", required="true", help="JSON file to use")
parser.add_argument("-d", "--debug", action='store_true',
                    help="Show Debug Output")

# Read arguments from command line
args = parser.parse_args()

if args.debug:
    print("Displaying Debug Output of % s" % parser.prog)
    print("File '{}' selected".format(args.file))

with open(args.file) as json_file:
    data = json.load(json_file)
    if args.debug:
        print("Data read from file:", args.file)
        print("Name:", data["name"])
        # print("Vars:", data["variables"])
        for keys, values in data["variables"].items():
            print("{key: >24}: {value}".format(key=keys, value=values))

# correct data
for keys, values in data["variables"].items():
    data_sub_link(data["variables"], keys, values)
for keys, values in data["variables"].items():
    data_rgb_to_hex(data["variables"], keys, values)


if args.debug:
    print("Corrected Data:")
    print("Name:", data["name"])
    # print("Vars:", data["variables"])
    for keys, values in data["variables"].items():
        print("{key: >24}: {value}".format(key=keys, value=values))

colsrgb = {}

for keys, values in data["variables"].items():
    colsrgb[keys] = hex_to_rgb(values)

if args.debug:
    print("dict: colsrgb")
    for keys, values in colsrgb.items():
        print("{k: >24}: {v}".format(k=keys, v=values))

theme = "gradience"

username = os.environ['USER']
home_dir = os.environ.get('HOME', '/home/{}'.format(username))

adwsteamgtk = "{}/.var/app/io.github.Foldex.AdwSteamGtk".format(home_dir)
adwtheme = "{}/cache/AdwSteamInstaller/extracted/adwaita".format(adwsteamgtk)
colorthemes = "{}/colorthemes".format(adwtheme)
target_dir = "{c}/{t}".format(c=colorthemes, t=theme)
target_file = "{d}/{tn}.css".format(d=target_dir, tn=theme)

if args.debug:
    print("target file: {}".format(target_file))

if not os.path.exists(target_dir):
    os.makedirs(target_dir)

template = '''\
:root {{
    /* The main accent color and the matching text value */
    --adw-accent-bg-rgb: {accent_bg_color};
    --adw-accent-fg-rgb: {accent_fg_color};
    --adw-accent-rgb: {accent_color};

    /* destructive-action buttons */
    --adw-destructive-bg-rgb: {destructive_bg_color};
    --adw-destructive-fg-rgb: {destructive_fg_color};
    --adw-destructive-rgb: {destructive_color};

    /* Levelbars, entries, labels and infobars. These don't need text colors */
    --adw-success-bg-rgb: {success_bg_color};
    --adw-success-fg-rgb: {success_fg_color};
    --adw-success-rgb: {success_color};

    --adw-warning-bg-rgb: {warning_bg_color};
    --adw-warning-fg-rgb: {warning_fg_color};
    --adw-warning-fg-a: 0.8;
    --adw-warning-rgb: {warning_color};

    --adw-error-bg-rgb: {error_bg_color};
    --adw-error-fg-rgb: {error_fg_color};
    --adw-error-rgb: {error_color};

    /* Window */
    --adw-window-bg-rgb: {window_bg_color};
    --adw-window-fg-rgb: {window_fg_color};

    /* Views - e.g. text view or tree view */
    --adw-view-bg-rgb: {view_bg_color};
    --adw-view-fg-rgb: {view_fg_color};

    /* Header bar, search bar, tab bar */
    --adw-headerbar-bg-rgb: {headerbar_bg_color};
    --adw-headerbar-fg-rgb: {headerbar_fg_color};
    --adw-headerbar-border-rgb: {headerbar_border_color};
    --adw-headerbar-backdrop-rgb: {headerbar_backdrop_color};
    --adw-headerbar-shade-rgb: {headerbar_shade_color};
    --adw-headerbar-shade-a: 0.36;
    --adw-headerbar-darker-shade-rgb: {headerbar_shade_color};
    --adw-headerbar-darker-shade-a: 0.9;

    /* Split pane views */
    --adw-sidebar-bg-rgb: {sidebar_bg_color};
    --adw-sidebar-fg-rgb: {sidebar_fg_color};
    --adw-sidebar-backdrop-rgb: {sidebar_backdrop_color};
    --adw-sidebar-shade-rgb: {sidebar_shade_color};
    --adw-sidebar-shade-a: 0.36;

    --adw-secondary-sidebar-bg-rgb: {sidebar_bg_color};
    --adw-secondary-sidebar-fg-rgb: {sidebar_fg_color};
    --adw-secondary-sidebar-backdrop-rgb: {sidebar_backdrop_color};
    --adw-secondary-sidebar-shade-rgb: {sidebar_shade_color};
    --adw-secondary-sidebar-shade-a: 0.36;

    /* Cards, boxed lists */
    --adw-card-bg-rgb: {shade_color};
    --adw-card-bg-a: 0.08;
    --adw-card-fg-rgb: {card_fg_color};
    --adw-card-shade-rgb: {card_shade_color};
    --adw-card-shade-a: 0.36;

    /* Dialogs */
    --adw-dialog-bg-rgb: {dialog_bg_color};
    --adw-dialog-fg-rgb: {dialog_fg_color};

    /* Popovers */
    --adw-popover-bg-rgb: {popover_bg_color};
    --adw-popover-fg-rgb: {popover_fg_color};
    --adw-popover-shade-rgb: {popover_bg_color};
    --adw-popover-shade-a: 0.36;

    /* Thumbnails */
    --adw-thumbnail-bg-rgb: {view_bg_color};
    --adw-thumbnail-fg-rgb: {view_fg_color};

    /* Miscellaneous */
    --adw-shade-rgb: {shade_color};
    --adw-shade-a: 0.36;
}}\
'''.format(**colsrgb)

# print(template)

with open(target_file, 'w') as file:
    file.write(template)
