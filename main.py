#
#  Created by Jonas Miederer.
#  Date: 27.03.16
#  Time: 17:35
#  Project: iTunesPlaylister
#  We're even wrong about which mistakes we're making. // Carl Winfield
#
import logging

from iTunesParser import iTunesParser
import schedule
import time
import argparse
import os.path
import sys

logger = logging.getLogger('iTunesPlaylister')


def writeFiles(playlists, path):
    for playlist in playlists:
        try:
            file = open("{}.M3U".format(os.path.join(path, playlist.title)), 'w')
            file.write("#EXTM3U\n")
            for song in playlist.songs:
                file.write("#EXTINF:{},{} - {}\n{}\n".format(song.duration, song.artist, song.name, song.path))
            file.close()
            logger.info('Playlist "{}" successfully written'.format(playlist.title))
        except:
            logger.error('File for playlist {} could not be written. Please check your permissions.'.format(playlist.title))


def job(target, destination):
    itParser = iTunesParser(target)
    writeFiles(itParser.parse(), destination)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')  # todo
    parser.add_argument('--target', help='The iTunes.xml file', required=True)
    parser.add_argument('--destination', help='The target folder', required=True)
    parser.add_argument('--interval',
                        help='The intverval of execution. Give an integer value indicating the minutes between two executions. 0 means executing it only once. -1 means executing it once a day, -2 twice a day and so on. Default is 0.',
                        type=int, default=0)
    args = parser.parse_args()
    # check if iTunes-File is given and exists
    if not os.path.isfile(args.target):
        sys.exit("No iTunes Library.xml file given or file does not exist.")

    if not os.path.isdir(args.destination):
        sys.exit("No target directory given or directory does not exist.")

    if args.interval == 0:
        job(args.target, args.destination)
    elif args.interval > 0:
        schedule.every(args.interval).minutes.do(job, args.target, args.destination)
    elif args.interval < 0:
        minutes = 60 * 24 / (args.interval * -1)
        schedule.every(minutes).minutes.do(job, args.target, args.destination)

    logger.info('Started watching.')
    while args.interval != 0:
        schedule.run_pending()
        time.sleep(1)

    logger.info('Stopped watching.')
