import Clients
from collections import OrderedDict
import dbus
import os, os.path
from string import Template

import prefs

def is_running(client):
    """
    Returns True if the media player corresponding to the passed in Client object is currently on, and thus communicable.
    """
    bus = dbus.SessionBus()
    return (bus.name_has_owner(client.dest_name))

def format_data(data, template_string, truncation_limit):
    # Truncate all data to the limit passed into this method
    for k in data:
        data[k] = (data[k][:truncation_limit]+'...' if len(data[k]) > truncation_limit else data[k])

    # Create a template and replace all templated data with the actual stuff, or question marks if the data cannot be found.
    template = Template(template_string)
    output = template.substitute(
            title=data.setdefault('title', '?'),
            artist=data.setdefault('artist', '?'),
            albumArtist=data.setdefault('albumArtist', '?'),
            album=data.setdefault('album', '?'),
            track=data.setdefault('trackNumber', '?'),
            disc=data.setdefault('discNumber', '?'),
            genre=data.setdefault('genre', '?'),
            length=data.setdefault('length', '?'),
            position=data.setdefault('position', '?'),
            year=data.setdefault('year', '?'),
            rating=data.setdefault('rating', '?'),
            autoRating=data.setdefault('autoRating', '?'))
    return output

def main():
    c = None

    # Open the prefs file.
    subs = Clients.Client.__subclasses__()

    try:
        for l in prefs.player_priorities:
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
    except AttributeError:
        print("Player priorities have not been set.")
        exit(1)

    if c is not None:
        c.connect()
        data = c.get_data()
        if data is not None:
            try:
                trunc_len = prefs.truncation_length
            except AttributeError:
                trunc_len = 25

            try:
                format_string = prefs.format_string
            except AttributeError:
                format_string = "$track. $title - $artist"

            print(format_data(data, format_string, trunc_len))
        else:
            print("Could not retrieve data from media player " + l + ".")
    else:
        print("No running client detected.")

if __name__ == '__main__':
    main()
