#!/usr/bin/env python3

from help import show_help
from downloader import download_video
import sys, pytube

def get_max_video(c):
    counter = 0
    for video in c.video_urls:
        counter += 1
    return counter

def main():
    show_help()
    c = pytube.Channel(str(sys.argv[1]))
    if c == None:
        print("The Channel doesn't exist.")
        sys.exit(84)

    print(f'Downloading videos by: {c.channel_name}')

    max_video = get_max_video(c)
    count = 0

    download_video(c, count, max_video)

    print('Done!')

if __name__ == '__main__':
    main()
