import mpv
import argparse

queue = []
player = mpv.MPV(ytdl=True, input_default_bindings=True, input_terminal=True, terminal=True, video=False)

def print_playlist(player):
    for n, item in enumerate(player.playlist):
        play_status = lambda item : "*" if item.get('current') else ""
        print("{:<2}{:<2} {}".format(
            play_status(item),
            n,
            item.get('filename')
        ))

def prompt(player, text, callback):
    player.terminal = False
    res = input("\n" + text + " >")
    callback(res)
    print_playlist(player)
    player.terminal = True
    

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

    @player.property_observer('playlist-pos')
    def position_observer(_name, value):
        print_playlist(player)

    ask_url()
    while True:
        if len(player.playlist) > 0:
            if player.playlist_pos is None:
                player.playlist_pos = 0
        player.wait_for_playback()
