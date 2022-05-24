from resolution import find_high_resolution
from pytube.cli import on_progress
import shutil, ffmpeg, os, pytube

def download_high(tag, count, max_video, video, path):
    total, used, free = shutil.disk_usage('/')
    
    link = pytube.YouTube(video)
    print(f'Downloading Video: {link.title}.mp4')
    pytube.YouTube(video, on_progress_callback=on_progress).streams.get_by_itag(tag.itag).download(output_path=f'{path}/temp/', max_retries=500, skip_existing=True, filename=f'{link.title}.mp4')
    print(f'Downloading Audio: {link.title}.webm')
    pytube.YouTube(video, on_progress_callback=on_progress).streams.filter(only_audio=True).first().download(output_path=f'{path}/temp/', max_retries=500, skip_existing=True, filename=f'{link.title}.webm')
    fps = int(pytube.YouTube(video, on_progress_callback=on_progress).streams.get_by_itag(tag.itag).fps)
    
    print("Going to combine video and audio.")

    source_video = ffmpeg.input(f'{path}/temp/{link.title}.mp4').filter('fps', fps=fps, round='up')
    source_audio = ffmpeg.input(f'{path}/temp/{link.title}.webm')
    output_video = f'{path}/video_output/{link.title}.mp4'
    
    ffmpeg.output(source_video, source_audio, output_video).run()
    
    size = link.streams.get_by_itag(tag.itag).filesize
    usage = ((free - size) // (2**30))
    max_disk = ((total) // (2**30))
    print('The video is downloaded.')
    print(f'Disk available: {usage} / {max_disk} GB.')
    count += 1
    print(f'You have download {count} of {max_video}.')
    
    os.remove(f'{path}/temp/{link.title}.mp4')
    os.remove(f'{path}/temp/{link.title}.webm')
    
    return count

def download_video(c, count, max_video, path):
    
    for video in c.video_urls:
        total, used, free = shutil.disk_usage('/')
        try:
            if pytube.YouTube(video).age_restricted == False:
                link = pytube.YouTube(video)
                tag = find_high_resolution(link)
            else:
                tag = None
            
            if tag != None:
                if tag.resolution == "1080p":
                    count = download_high(tag, count, max_video, video, path)
                else:
                    print(f'Downloading Video with Audio: {link.title}.mp4')
                    pytube.YouTube(video, on_progress_callback=on_progress).streams.get_by_itag(tag.itag).download(output_path=f'{path}/video_output/', max_retries=500, skip_existing=True)
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