import mpv
import argparse

queue = []
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

def prompt(player, text, callback):
    player.terminal = False
    res = input("\n" + text + " >")
    callback(res)
    print_playlist()
    player.terminal = True
    
def handle_command(command):
    def base(text):
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
                player.playlist_move(int(f)-1, int(t)-1)
            except:
                print("please enter valid indices")
        else:
            print("please enter index and destination")


    base(command)

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='simple queue player for mpv')
    # parser.add_argument('--no-video', action='store_true')

    # args = parser.parse_args()
    
    @player.on_key_press('a')
    def ask_url():
        def cb(url):
            if url != "":
                player.playlist_append(url)
        prompt(player, "Enter URL", cb)

    @player.on_key_press('c')
    def ask_command():
        prompt(player, "Enter command (or 'h' for help)", handle_command)

    @player.property_observer('playlist-pos')
    def position_observer(_name, value):
        print_playlist()

    ask_url()
    while True:
        if len(player.playlist) > 0:
            if player.playlist_pos is None:
                player.playlist_pos = 0
        player.wait_for_playback()
