#!/usr/bin/env python3

import sys
import mpv
import argparse

HELP_WELCOME = """Welcome to pasteplayer!
Press `a` to append a new item to the playlist.
Press `c` to open the command prompt.
"""

HELP_COMMANDS = """The following commands are available:
    'j POSITION' to skip to given item
    'r POSITION' to remove item from the playlist
    'm POSITION NEW_POSITION' to move item
"""

default_properties = {
    "config": True,
    "ytdl": True,
    "input_default_bindings": True,
    "input_terminal": True,
    "input_vo_keyboard": True,
    "osc": True,
    "terminal": True,
    "video": False,
    "loop-playlist": "no"
}

def print_playlist():
    for n, item in enumerate(player.playlist):
        play_status = lambda item : "*" if item.get('current') else ""
        display_name = lambda item: item.get('title') if 'title' in item else item.get('filename')

        print("{:<2}{:>2}. {}".format(
            play_status(item),
            n+1,
            display_name(item)
        ))

def prompt(text, callback):
    player.terminal = False
    res = input("\n" + text + " >")
    callback(res)
    print_playlist()
    player.terminal = True

def start_playback(initial=False):
    """Checks if there are items in the playlist and playback hasn't been started.
    If initial is set, it will start with the first title, else, we presume just one title has been added to the end."""
    if len(player.playlist) > 0:
        if player.playlist_pos is None:
            # when adding a title to an empty playlist, mpv doesn't automatically start playback,
            # this does the job.
            if initial:
                player.playlist_pos = 0
            else:
                player.playlist_pos = len(player.playlist) - 1

def greet():
    print(HELP_WELCOME)

def handle_command(command):
    """Crude command parser"""
    def base(text):
        """Base parser dispatching to subparsers for each command"""
        if text.strip() == "h" or text.strip() == "help":
            print(HELP_COMMANDS)
        if text.startswith("m "):
            move(text[2:])
        if text.startswith("r "):
            remove(text[2:])
        if text.startswith("j "):
            jump(text[2:])

    def jump(text):
        try:
            n = int(text.strip())
            player.playlist_pos = n-1
        except ValueError:
            print("please enter valid number")
        except TypeError:
            print("please enter a valid index")

    def remove(text):
        try:
            n = int(text.strip())
            player.playlist_remove(n-1)
        except ValueError:
            print("please enter valid index")

    def move(text):
        args = text.split(" ")
        print(args)
        if len(args) == 2:
            f, t = args
            try:
                # I don't quite get this yet, but for some reason, f seems to be indexed at 0 while t is at 1
                player.playlist_move(int(f)-1, int(t))
            except:
                print("please enter valid indices")
        else:
            print("please enter index and destination")

    base(command)

def main():
    global player
    parser = argparse.ArgumentParser(description='simple queue player for mpv')
    parser.add_argument('files', metavar="URL/PATH", default=None, nargs='*')
    parser.add_argument('-p', '--property', metavar=("KEY", "VALUE"), nargs=2, default=[], action='append',
                        help="set mpv property KEY to VALUE. See all available properties with 'mpv --list-properties'")
    parser.add_argument('-v', '--video', action='store_true', help="Enable video. Shorthand for '-p video auto'")

    args = parser.parse_args()

    props = default_properties

    # assemble dict from properties from command line
    custom_props = {p[0]: p[1] for p in args.property}

    # override/add properties from arguments
    props.update(custom_props) 

    if args.video:
        props['video'] = "auto"

    player = mpv.MPV(**props)


    @player.on_key_press('a')
    def ask_url():
        """Ask for filename/URL to append to the playlist"""

        def cb(url):
            if url != "":
                player.playlist_append(url)
                start_playback()
        prompt("Enter URL or file name", cb)

    @player.on_key_press('c')
    def ask_command():
        """Open playlist editing command prompt.
        Available commands listed in HELP_COMMANDS"""

        prompt("Enter command (or 'h' for help)", handle_command)

    @player.property_observer('playlist_pos')
    def playlist_pos_observer(_name, value):
        """Display playlist on track change"""
        print_playlist()


    greet()

    if len(args.files) > 0:
        for f in args.files:
            player.playlist_append(f)

        print_playlist()
    else:
        ask_url()

    start_playback(initial=True)

    # slightly ugly; but makes sure this thread terminates when mpv terminates
    # there probably is a better way to do this.
    player._event_thread.join()

if __name__ == '__main__':
    main()
