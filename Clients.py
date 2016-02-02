import datetime
import dbus
import time

def format_time(millis, format_string="%-M:%S"):
    t = datetime.timedelta(microseconds=millis).total_seconds()
    return time.strftime(format_string, time.gmtime(t))

def replace_key(data, old_key, new_key):
    data[new_key] = data[old_key]
    del data[old_key]

class Client:
    """
    A parent Client module. Clients perform the following tasks for a particular type of media player:
        * Get data from a media player, such as the currently playing track
        * Parse the data into something readable
        * Emit this readable data in a common format.
    """

    dest_name = None
    object_path = None
    message_name = None

    def __init__(self):
        self.bus = dbus.SessionBus()
        self.obj = self.bus.get_object(self.dest_name, self.object_path)
        if self.message_name is not None:
            self.interface = dbus.Interface(self.obj, dbus_interface=self.message_name)
    
    def get_data(self):
        """
        Returns data.
        """
        return dict()

class Spotify(Client):
    """
    A client that interfaces with a running Spotify instance.
    """

    bus = None
    obj = None
    interface = None

    dest_name = "org.mpris.MediaPlayer2.spotify"
    object_path = "/org/mpris/MediaPlayer2"
    message_name = "org.freedesktop.DBus.Properties"

    def get_data(self):
        metadata = self.interface.Get('org.mpris.MediaPlayer2.Player', 'Metadata')

        data = dict()

        for k in metadata.keys():
            # Convert the data to a regular string from a dbus string
            if type(metadata[k]) == dbus.Array:
                metadata[k] = metadata[k][0]
            metadata[k] = str(metadata[k])

            # Remove the "mpris:"/"xesam:" from each key
            new_key = k.split(':')
            # As we're replacing data in the same structure, we need to check if we're going to attempt to replace a previously shortened key
            data[new_key[len(new_key)-1]] = metadata[k]

        # Update formatting for a couple of items
        # TODO floating point precision
        # TODO remove magic number
        data['autoRating'] = str(data['autoRating'] * 10)
        data['length'] = format_time(int(data['length']))
        return data

class Banshee(Client):
    """
    A client that interfaces with a running Banshee instance.
    """

    dest_name = "org.bansheeproject.Banshee"
    object_path = "/org/bansheeproject/Banshee/PlayerEngine"
    message_name = None

    def get_data(self):
        data = self.obj.GetCurrentTrack()
        for k in data.keys():
            # Convert all to strings from dbus strings
            data[k] = str(data[k])

        print(data)

        try:
            replace_key(data, 'name', 'title')
            replace_key(data, 'track-number', 'trackNumber')
        except KeyError:
            pass

        return data
