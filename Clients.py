import datetime
import dbus
import time

def format_time(millis, format_string="%-M:%S"):
    t = datetime.timedelta(microseconds=millis).total_seconds()
    return time.strftime(format_string, time.gmtime(t))

def replace_missing(data):
    keys = [
            'trackid',
            'length',
            'artUrl',
            
            'album',
            'albumArtist',
            'artist',
            'asText',
            'audioBPM',
            'autoRating',
            'comment',
            'composer',
            'contentCreated',
            'discNumber',
            'firstUsed',
            'genre',
            'lastUsed',
            'lyricist',
            'title',
            'trackNumber',
            'url',
            'useCount',
            'userRating',
            'year'
            ]
    for k in keys:
        if k not in data.keys():
            data[k] = '?'

    return data

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
        print(metadata)

        data = dict()
        data['album'] = str(metadata['xesam:album'])
        data['albumArtist'] = str(metadata['xesam:albumArtist'][0])
        data['artist'] = str(metadata['xesam:artist'][0])
        data['artUrl'] = str(metadata['mpris:artUrl'])
        # TODO floating point precision
        # TODO remove floating point number
        data['autoRating'] = str(metadata['xesam:autoRating'] * 10)
        data['discNumber'] = str(metadata['xesam:discNumber'])
        data['length'] = format_time(int(metadata['mpris:length']))
        data['title'] = str(metadata['xesam:title'])
        data['trackNumber'] = str(metadata['xesam:trackNumber'])
        data['trackid'] = str(metadata['mpris:trackid'])
        data['url'] = str(metadata['xesam:url'])
        return replace_missing(data)

class Banshee(Client):
    """
    A client that interfaces with a running Banshee instance.
    """

    dest_name = "org.bansheeproject.Banshee"
    object_path = "/org/bansheeproject/Banshee/PlayerEngine"
    message_name = None

    def get_data(self):
        metadata = self.obj.GetCurrentTrack()

        data = dict()
        data['artist'] = str(metadata['artist'])
        data['album'] = str(metadata['album'])
        data['title'] = str(metadata['name'])
        data['year'] = str(metadata['year'])


        return data
