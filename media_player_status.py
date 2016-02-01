import subprocess

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
    current_title = bytes_to_string(subprocess.check_output(["banshee", "--query-title"])).split(': ')[1]
    current_artist = bytes_to_string(subprocess.check_output(["banshee", "--query-artist"])).split(': ')[1]
    current_album = bytes_to_string(subprocess.check_output(["banshee", "--query-album"])).split(': ')[1]
    current_year = bytes_to_string(subprocess.check_output(["banshee", "--query-year"])).split(': ')[1]
    data = {'title': current_title,
            'artist': current_artist,
            'album': current_album,
            'year': current_year}
    return data

def format_string(data):
    output = '{0} - {1}, {2} ({3})'.format(data['title'], data['artist'], data['album'], data['year'])
    return output



if __name__ == '__main__':
    if get_pid("spotify"):
        print("Spotify not yet implemented.")
    elif get_pid("banshee"):
        data = get_banshee()
        output = format_string(data)
        print(output)
        
    
