import datetime
import dbus
import time

def format_time(millis, format_string="%-M:%S"):
    t = datetime.timedelta(milliseconds=millis).total_seconds()
    return time.strftime(format_string, time.gmtime(t))

def remove_xesam_mpris_delimiters(metadata):
    data = dict()
    for k in metadata.keys():
        if type(metadata[k]) == dbus.Array:
            metadata[k] = metadata[k][0]
        metadata[k] = str(metadata[k])

        if k.startswith('xesam:') or k.startswith('mpris:'):
            # Remove the "mpris:"/"xesam:" from each key
            new_key = k.split(':')[1]
        else:
            new_key = k

        # As we're replacing data in the same structure, we need to check if we're going to attempt to replace a previously shortened key
        data[new_key] = metadata[k]
    return data

def convert_to_strings(data):
    """
    Convert dbus data to strings.
    """
    for k in data.keys():
        # Convert all to strings from dbus strings
        data[k] = str(data[k])
    return data

class Client:
    """
    A parent Client module. Clients perform the following tasks for a particular type of media player:
        * Get data from a media player, such as the currently playing track
        * Parse the data into something readable
        * Emit this readable data in a common format.
    """

    bus = None
    obj = None
    interface = None

    dest_name = None
    object_path = None
    message_name = None

    def __init__(self):
        pass

    def connect(self):
        self.bus = dbus.SessionBus()
        self.obj = self.bus.get_object(self.dest_name, self.object_path)
        if self.message_name is not None:
            self.interface = dbus.Interface(self.obj, dbus_interface=self.message_name)
    
    def get_data(self):
        """
        Returns metadata on the current song in a common format.
        """
        return dict()

class Clementine(Client):
    """
    A client that interfaces with a running Clementine instance.
    """

    dest_name = "org.mpris.clementine"
    object_path = "/Player"
    message_name = "org.freedesktop.MediaPlayer"

    def get_data(self):
        metadata = convert_to_strings(self.interface.GetMetadata())
        metadata['position'] = format_time(int(self.interface.PositionGet()))
        metadata['trackNumber'] = metadata.pop('tracknumber')
        metadata['length'] = format_time(millis=int(metadata['mtime']))
        return metadata

    


class Spotify(Client):
    """
    A client that interfaces with a running Spotify instance.
    """

    dest_name = "org.mpris.MediaPlayer2.spotify"
    object_path = "/org/mpris/MediaPlayer2"
    message_name = "org.freedesktop.DBus.Properties"

    def get_data(self):
        metadata = convert_to_strings(self.interface.Get('org.mpris.MediaPlayer2.Player', 'Metadata'))

        data = remove_xesam_mpris_delimiters(metadata)

        # Update formatting for a couple of items
        data['autoRating'] = str(float(data['autoRating']) * 5) # rating is a float between 0 and 1, so we multiply by 5 to standardise.
        data['length'] = format_time(int(data['length'])/1000) # length is returned in microseconds, so we convert to milliseconds
        return data

class Banshee(Client):
    """
    A client that interfaces with a running Banshee instance.
    """

    dest_name = "org.bansheeproject.Banshee"
    object_path = "/org/bansheeproject/Banshee/PlayerEngine"
    message_name = None

    def get_data(self):
        # data = self.obj.GetCurrentTrack()
        data = convert_to_strings(self.obj.GetCurrentTrack())

        # Rating and song positions are separate attributes, so we make separate calls to them
        data['rating'] = self.obj.GetRating()
        data['position'] = format_time(self.obj.GetPosition())

        # Need to update a couple of bits of formatting to comply with our dict structure
        data['albumArtist'] = data.pop('album-artist')
        if data.get('score') is not None:
            data['autoRating'] = int(data.pop('score'))/20 # normalise rating to be in range of 1-5
        data['title'] = data.pop('name')
        data['trackNumber'] = data.pop('track-number')
        data['length'] = format_time(float(data['length']) * 1000 * 1000)

        return data
