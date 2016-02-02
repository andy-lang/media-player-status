import Clients
from collections import OrderedDict
import dbus

def is_running(client):
    """
    Returns True if the media player corresponding to the passed in Client object is currently on, and thus communicable.
    """
    bus = dbus.SessionBus()
    return (bus.name_has_owner(client.dest_name))

def format_data(data):
    output = '{0}. {1} - {2} ({3}, {4})'.format(
            data.setdefault('trackNumber', '?'),
            data.setdefault('title', '?'),
            data.setdefault('artist', '?'),
            data.setdefault('album', '?'),
            data.setdefault('year', '?'))
    return output

def replace_missing(data):
    keys = [
            'album',
            'albumArtist',
            'artist',
            'autoRating',
            'composer',
            'discNumber',
            'genre',
            'length',
            'title',
            'trackNumber',
            'useCount',
            'userRating',
            'year'
            ]
    for k in keys:
        if k not in data.keys():
            data[k] = '?'

    return data

def main():
    supported_clients = OrderedDict()
    supported_clients['spotify'] = Clients.Spotify()
    supported_clients['banshee'] = Clients.Banshee()
    c = None

    for k in supported_clients.keys():
        if is_running(supported_clients[k]):
            c = supported_clients[k]
            break
            
    if c is not None:
        data = c.get_data()
        if data is not None:
            # print(data)
            print(format_data(data))
    else:
        print("No running client detected.")

if __name__ == '__main__':
    main()
