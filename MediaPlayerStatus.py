from Clients import *

def is_running(client):
    """
    Returns True if the media player corresponding to the passed in Client object is currently on, and thus communicable.
    """
    bus = dbus.SessionBus()
    return (bus.name_has_owner(client.dest_name))

if __name__ == '__main__':
    if is_running(SpotifyClient):
        c = SpotifyClient()

    data = c.get_data()
    print(data['title'])
