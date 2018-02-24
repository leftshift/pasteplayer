#!/usr/bin/env python3

import mpv
import argparse

player = mpv.MPV(ytdl=True, input_default_bindings=True, input_terminal=True, terminal=True, video=False)

HELP_COMMANDS = """The following commands are available:
    'r POSITION' to remove item from the playlist
    'm POSITION NEW_POSITION' to move item
"""

def print_playlist():
    for n, item in enumerate(player.playlist):
        play_status = lambda item : "*" if item.get('current') else ""
        print("{:<2}{:>2}. {}".format(
            play_status(item),
            n+1,
            item.get('filename')
        ))

def prompt(text, callback):
    player.terminal = False
    res = input("\n" + text + " >")
    callback(res)
    print_playlist()
    player.terminal = True
    
def handle_command(command):
    """Crude command parser"""
    def base(text):
        """Base parser dispatching to subparsers for each command"""
        if text.strip() == "h":
            print(HELP_COMMANDS)
        if text.startswith("m "):
            move(text[2:])
        if text.startswith("r "):
            remove(text[2:])

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
    parser = argparse.ArgumentParser(description='simple queue player for mpv')

    parser.add_argument('files', metavar="url/paths", default=None, nargs='*')
    # parser.add_argument('--no-video', action='store_true')

    args = parser.parse_args()
    
    @player.on_key_press('a')
    def ask_url():
        """Ask for filename/URL to append to the playlist"""
        def cb(url):
            if url != "":
                player.playlist_append(url)
        prompt("Enter URL or file name", cb)

    @player.on_key_press('c')
    def ask_command():
        """Open playlist editing command prompt"""
        prompt("Enter command (or 'h' for help)", handle_command)

    @player.property_observer('playlist-pos')
    def position_observer(_name, value):
        """Print playlist when current title changes"""
        print_playlist()

    if len(args.files) > 0:
        for f in args.files:
            player.playlist_append(f)
    else:
        ask_url()

    while True:
        if len(player.playlist) > 0:
            if player.playlist_pos is None:
                player.playlist_pos = 0
        player.wait_for_playback()

if __name__ == '__main__':
    main()
