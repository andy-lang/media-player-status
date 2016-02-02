import Clients
from collections import OrderedDict
import dbus
import os, os.path

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

def main():
    c = None

    # Open the prefs file.
    filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'prefs.txt')
    f = open(filepath, 'r')
    lines = f.readlines()

    subs = Clients.Client.__subclasses__()

    for l in lines:
        l = l.rstrip()
        # If there's a subclass of Clients.Client with a name equal to the current line in the text file, then this is the one to take note of.
        i = (next((i for i, s in enumerate(subs) if s.__name__ == l), -1))
        if i >= 0:
            # check that it's running. If it is, we have a match.
            if is_running(subs[i]):
                c = subs[i]()
                break
        else:
            # If the line isn't recognised as a subclass, the user will want to know. Print an error and exit.
            print("Media player " + l + " not recognised.")
            exit(1)

    if c is not None:
        c.connect()
        data = c.get_data()
        if data is not None:
            print(format_data(data))
    else:
        print("No running client detected.")

if __name__ == '__main__':
    main()
