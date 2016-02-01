import subprocess
import re
import dbus

def get_pid(name):
    """
    Args:
        name (str): The name of the process to search for.

    Returns:
        A list of PIDs corresponding to the given name.
        If no such process is found, return an empty list.
    """
    try:
        return list(map(int, subprocess.check_output(["pidof", name]).split()))
    except subprocess.CalledProcessError:
        return list()

def bytes_to_string(s):
    return s.decode('utf-8').rstrip()


def get_banshee():
    # TODO replace this with dbus calls
    # Banshee has the capabilities for this at http://banshee.fm/contribute/write-code/dbus-interfaces/
    metadata = bytes_to_string(subprocess.check_output(["banshee", "--query-title", "--query-artist", "--query-album", "--query-year"])).rsplit('\n')
    metadata = dict([x.split(': ') for x in metadata])
    return metadata

def get_spotify():
    bus = dbus.SessionBus()
    obj = bus.get_object("org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2")
    interface = dbus.Interface(obj, dbus_interface='org.freedesktop.DBus.Properties')
    metadata = interface.Get('org.mpris.MediaPlayer2.Player', 'Metadata')

    data = dict()
    data['artist'] = metadata['xesam:albumArtist'][0]
    data['album'] = metadata['xesam:album']
    data['title'] = metadata['xesam:title']
    data['year'] = '?'
    return data

def format_string(data):
    # TODO pass in a format string and parse from there
    output = '{0} - {1}, {2} ({3})'.format(data['title'], data['artist'], data['album'], data['year'])
    return output



if __name__ == '__main__':
    if get_pid("spotify"):
        data = get_spotify()
    elif get_pid("banshee"):
        data = get_banshee()
    output = format_string(data)
    print(output)
        
    
