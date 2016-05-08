## media-player-status

A Python 3 script to get information about what's currently playing on your favourite Linux media player.

### Why does this exist?

Like a lot of people, I like listening to music when I code. I run Tmux in a fullscreen window, and I don't like leaving that window unless I absolutely have to. Problem was, I found myself constantly switching windows to look at what was playing, which was wasting a lot of time. So I built a script that checks the currently open media player, and retrieves information about the currently playing song.

### Features

* Python 3
* Works out of the box - no external dependencies required
* Gets data for several media players in Linux
	* [Clementine](https://www.clementine-player.org/)
	* [Spotify](https://www.spotify.com/us/download/linux/)
	* [Banshee](http://banshee.fm/)
	* [Pithos](http://pithos.github.io/)
* Super easy to interface with other programs, such as Tmux, Vim, or Emacs - just call the script!
* Customisable format strings

### Upcoming Features

* Support for more media players
* Your ideas here...

### FAQ/Troubleshooting

**How does it work?**

A majority of Linux media players implement a standard called `dbus`. In general, `dbus` allows you to get information about currently running programs and their state (for example, the current song in a media player) or to change their state (such as toggling a song as playing or paused). If you've ever seen desktop notifications on Ubuntu, Fedora, Arch, etc., then all they're really doing is communicating with programs through `dbus`. This script uses the same framework.

**My media player isn't supported.**

Let me know and I'll take a look and implement something for you. Alternatively, write it yourself and send me a pull request.

**There's a question mark in the output! What does it mean?**

While `dbus` is a standard, it's not one that everyone adheres to completely. For example, Spotify doesn't tell you the year a song came out, or the current position you are in the song, whereas Banshee can tell you both of these things. For this reason, there's some modules that just can't support getting certain bits of information, because the program's `dbus` implementation doesn't support it either. A question mark denotes that the information couldn't be found, most likely for that reason.

Here's a table of which media player supports what:

| **Media Player** | Title | Artist | Album Artist | Album | Track Number | Disc Number | Genre | Length | Year | Position | User Rating | Auto Rating |
| ---------------- | ----- | ------ | ------------ | ----- | ------------ | ----------- | ----- | ------ | ---- | -------- | ----------- | ----------- |
| Banshee          | ✔     | ✔      | ✔            | ✔     | ✔            |             | ✔     | ✔      | ✔    | ✔        | ✔           | ✔           |
| Clementine       | ✔     | ✔      |              | ✔     | ✔            |             | ✔     | ✔      | ✔    | ✔        | ✔           |             |
| Spotify          | ✔     | ✔      | ✔            | ✔     | ✔            | ✔           |       | ✔      |      |          |             | ✔           |
| Pithos           | ✔     | ✔      |              | ✔     |              |             |       |        |      |          |             |             |
