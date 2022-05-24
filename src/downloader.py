from resolution import find_high_resolution
from pytube.cli import on_progress
import shutil, ffmpeg, os, pytube

def download_high(c, count, max_video, video):
    total, used, free = shutil.disk_usage('/')
    
    link = pytube.YouTube(video)
    pytube.YouTube(video, on_progress_callback=on_progress).streams.get_by_itag(137).download(output_path='./temp/', max_retries=500, skip_existing=True, filename=f'{link.title}.mp4')
    pytube.YouTube(video, on_progress_callback=on_progress).streams.filter(only_audio=True).first().download(output_path='./temp/', max_retries=500, skip_existing=True, filename=f'{link.title}.webm')
    
    print("Going to combine video and audio.")

    source_video = ffmpeg.input(f'./temp/{link.title}.mp4')
    source_audio = ffmpeg.input(f'./temp/{link.title}.webm')
    output_video = f'./video_output/{link.title}.mp4'
    
    ffmpeg.output(source_video, source_audio, output_video).run()
    
    size = link.streams.get_by_itag(137).filesize
    usage = ((free - size) // (2**30))
    max_disk = ((total) // (2**30))
    print('The video is downloaded.')
    print(f'Disk available: {usage} / {max_disk} GB.')
    count += 1
    print(f'You have download {count} of {max_video}.')
    
    os.remove(f'./temp/{link.title}.mp4')
    os.remove(f'./temp/{link.title}.webm')
    
    return count

def download_video(c, count, max_video):
    
    for video in c.video_urls:
        total, used, free = shutil.disk_usage('/')
        try:
            if pytube.YouTube(video).age_restricted == False:
                link = pytube.YouTube(video)
                tag = find_high_resolution(link)
            else:
                tag = None
            
            if tag != None:
                print(f'Downloading: {link.title}')
                if tag.resolution == "1080p":
                    count = download_high(c, count, max_video, video)
                else:
                    pytube.YouTube(video, on_progress_callback=on_progress).streams.get_by_itag(tag.itag).download(output_path='./video_output/', max_retries=500, skip_existing=True)
                    size = link.streams.get_by_itag(tag.itag).filesize
                    usage = ((free - size) // (2**30))
                    max_disk = ((total) // (2**30))
                    print('The video is downloaded.')
                    print(f'Disk available: {usage} / {max_disk} GB.')
                    count += 1
                    print(f'You have download {count} of {max_video}.')
            elif tag == None:
                print("Something is wrong with the video.")

        except NameError:
            print(NameError)