import dbus

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

class SpotifyClient(Client):
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
        data['artist'] = metadata['xesam:albumArtist'][0]
        data['album'] = metadata['xesam:album']
        data['title'] = metadata['xesam:title']
        data['year'] = '?'
        return data

class BansheeClient(Client):
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
