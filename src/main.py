#!/usr/bin/env python3

from tkinter import Tk
from tkinter.filedialog import askdirectory
from welcome import welcome_the_user
from downloader import download_video
import pytube, os

def get_max_video(c):
    counter = 0
    for video in c.video_urls:
        counter += 1
    return counter

def main():
    welcome_the_user()
    c = None

    while 42:
        url = str(input("insert the url: "))
        try:
            c = pytube.Channel(url)
        except:
            print("The Channel doesn't exist.")
            print('retry.')
        if c != None:
            break

    root = Tk()
    root.withdraw()
    path = askdirectory(title='Select Working Directory')
    print(f'Working Directory: {path}')

    if (os.path.isdir(f'{path}/video_output') == False):
        os.mkdir(f'{path}/video_output')
    if (os.path.isdir(f'{path}/temp') == False):
        os.mkdir(f'{path}/temp')
    print(f'Downloading videos by: {c.channel_name}')

    max_video = get_max_video(c)
    count = 0

    download_video(c, count, max_video, path)

    print('Done!')
    os.rmdir(f'{path}/temp')

if __name__ == '__main__':
    main()
