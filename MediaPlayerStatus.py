import Clients
import dbus

def is_running(client):
    """
    Returns True if the media player corresponding to the passed in Client object is currently on, and thus communicable.
    """
    bus = dbus.SessionBus()
    return (bus.name_has_owner(client.dest_name))

def format_data(data):
    output = '{0} - {1} ({2}, {3})'.format(data['title'], data['artist'], data['album'], data['year'])
    return output

if __name__ == '__main__':
    c = None
    if is_running(Clients.Spotify):
        c = Clients.Spotify()
    elif is_running(Clients.Banshee):
        c = Clients.Banshee()
    else:
        print("No media player detected.")
        
    if c is not None:
        data = c.get_data()
        if data is not None:
            print(format_data(c.get_data()))
