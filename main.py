#
#  Created by Jonas Miederer.
#  Date: 27.03.16
#  Time: 17:35
#  Project: iTunesPlaylister
#  We're even wrong about which mistakes we're making. // Carl Winfield
#
from iTunesParser import iTunesParser
import argparse
import os.path
import sys


def writeFiles(playlists, path):
    for playlist in playlists:
        try:
            file = open("{}.M3U".format(os.path.join(path, playlist.title)), 'w')
            file.write("#EXTM3U\n")
            for song in playlist.songs:
                file.write("#EXTINF:{},{} - {}\n{}\n".format(song.duration, song.artist, song.name, song.path))
            file.close()
        except:
            pass  # TODO


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')  # todo
    parser.add_argument('--target', help='The iTunes.xml file', required=True)
    parser.add_argument('--destination', help='The target folder')
    args = parser.parse_args()

    # check if iTunes-File is given and exists
    if not os.path.isfile(args.target):
        sys.exit("No iTunes Library.xml file given or file does not exist.")

    if not os.path.isdir(args.destination):
        sys.exit("No target directory given or directory does not exist.")
    iTunesParser = iTunesParser(args.target)
    writeFiles(iTunesParser.parse(), args.destination)
