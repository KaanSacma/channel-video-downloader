#!/usr/bin/env python3

from tkinter.filedialog import askdirectory
from welcome import welcome_the_user
from downloader import download_video
import pytube, os
import logging as logger

def get_max_video(c):
    counter = 0
    for video in c.video_urls:
        counter += 1
    return counter

def main():
    welcome_the_user()
    c = None
    path = None

    while 42:
        url = str(input("insert the url: "))
        try:
            c = pytube.Channel(url)
        except:
            print("The Channel doesn't exist.")
            print('retry.')
        if c != None:
            break
    while (os.path.isdir(r"{0}".format(path)) == False):
        path = askdirectory(title='Select Working Directory')
    print(r"Working Directory: {0}".format(path))

    if (os.path.isdir(r"{0}/video_output".format(path)) == False):
        os.mkdir(r"{0}/video_output".format(path))
    if (os.path.isdir(r"{0}/temp".format(path)) == False):
        os.mkdir(r"{0}/temp".format(path))
    print(r"Downloading videos by: {0}".format(c.channel_name))

    max_video = get_max_video(c)
    count = 0

    download_video(c, count, max_video, path)

    print('Done!')
    os.rmdir(r"{0}/temp".format(path))

if __name__ == '__main__':
    main()
