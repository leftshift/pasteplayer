# Pasteplayer

Pasteplayer is a (very) thin python wrapper around mpv to allow easy on-the-fly playlist editing (like pasting youtube URLs)

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
