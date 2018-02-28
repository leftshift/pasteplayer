# Pasteplayer

Pasteplayer is a (very) thin python wrapper around mpv to allow easy on-the-fly playlist editing (like pasting youtube URLs)

It's also available on pypi! Simply run `pip install pasteplayer`; after that, run the `pasteplayer` command from anywhere.

## Usage

Upon startup, you will be asked for a valid URL or file name.

All usual mpv keyboard shortcuts still work, e.g.:

* `space` to play/pause
* `>` to skip to the next title in the playlist
* `<` to go to the previous title
* `m` to mute
* …

Additionaly, you can press `a` to add a new item to the playlist or `c` for more playlist editing commands:

* `r NUMBER` to remove item at position NUMBER
* `m FROM TO` to move an item

### Command line arguments
```
usage: pasteplayer.py [-h] [-p KEY VALUE] [URL/PATH [URL/PATH ...]]

simple queue player for mpv

positional arguments:
  URL/PATH

optional arguments:
  -h, --help            show this help message and exit
  -p KEY VALUE, --property KEY VALUE
                        set mpv property KEY to VALUE. See all available
                        properties with 'mpv --list-properties'
  -v, --video           Enable video. Shorthand for '-p video auto'
```

### Potentially useful properties

* `video`: `auto`/`no` to enable/disable video
* `mute`: `yes`/`no` to mute audio (without disabling it)
* `fullscreen`: `yes`/`no`
* `osc`: `yes`/`no` to enable/disable on-screen-controller (the one that appears when you move the mouse)
