#
#  Created by Jonas Miederer.
#  Date: 27.03.16
#  Time: 17:44
#  Project: iTunesPlaylister
#  We're even wrong about which mistakes we're making. // Carl Winfield
#

import plistlib


class Track:
    def __init__(self):
        self.id = None
        self.name = None
        self.artist = None
        self.duration = -1
        self.path = None


class Playlist:
    def __init__(self, playlist, file):
        self.pl = playlist
        self.itlist = file
        self.id = playlist['Playlist ID']
        self.title = playlist['Name']
        self.songs = self.getSongs()

    def getSongs(self):
        songs = list()
        if 'Playlist Items' in self.pl:
            for song in self.pl['Playlist Items']:
                track = Track()
                track.id = song['Track ID']
                track_obj = self.itlist['Tracks']['{}'.format(track.id)]
                track.name = track_obj['Name']
                track.artist = track_obj['Artist']
                track.duration = int(track_obj['Total Time'] / 1000)
                track.path = track_obj['Location']
                songs.append(track)
        return songs


class iTunesParser:
    def __init__(self, iTunesFile):
        self.file = iTunesFile
        self.playlists = list()

    def parse(self):
        self.itlist = plistlib.readPlist(self.file)
        for playlist in self.itlist['Playlists']:
            if playlist['Name'] not in (
                    '####!####', 'Musik', 'Musikvideos', 'Leihobjekte', 'Filme', 'Eigene Videos', 'TV-Sendungen',
                    'Podcasts',
                    'iTunes U', 'Bücher', 'Hörbücher', 'PDFs', 'Genius',
                    'Klassische Musik') and 'iTunesU' not in playlist:
                self.playlists.append(Playlist(playlist, self.itlist))
        return self.playlists
