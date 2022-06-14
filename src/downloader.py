from resolution import find_high_resolution
from pytube.cli import on_progress
import shutil, ffmpeg, os, pytube, platform

def download_high(tag, count, max_video, video, path):
    total, used, free = shutil.disk_usage('/')
    
    link = pytube.YouTube(video)
    temp = r"{0}/temp/".format(path)
    video_temp = r"{0}/temp/{1}.mp4".format(path, link.title)
    audio_temp = r"{0}/temp/{1}.webm".format(path, link.title)
    video_file = r"{0}.mp4".format(link.title)
    audio_file = r"{0}.webm".format(link.title)
    
    print("Downloading Video: {0}".format(video_file))
    pytube.YouTube(video, on_progress_callback=on_progress).streams.get_by_itag(tag.itag).download(output_path=temp, max_retries=500, skip_existing=True, filename=video_file)
    print("Downloading Audio: {0}".format(audio_file))
    pytube.YouTube(video, on_progress_callback=on_progress).streams.filter(only_audio=True).first().download(output_path=temp, max_retries=500, skip_existing=True, filename=audio_file)
    fps = int(pytube.YouTube(video, on_progress_callback=on_progress).streams.get_by_itag(tag.itag).fps)
    
    print("Merging video and audio.")

    source_video = ffmpeg.input(video_temp).filter('fps', fps=fps, round='up')
    source_audio = ffmpeg.input(audio_temp)
    output_video = r"{0}/video_output/{1}.mp4".format(path, link.title)
    execute_path = os.getcwd()
    
    #if platform.system() == 'Windows':
        #ffmpeg.concat(source_video, source_audio, v=1, a=1).output(output_video).run(cmd=r"{0}/ffmpeg/bin/ffmpeg.exe".format(execute_path))
    
    size = link.streams.get_by_itag(tag.itag).filesize
    usage = ((free - size) // (2**30))
    max_disk = ((total) // (2**30))
    print('The video is downloaded.')
    print(f'Disk available: {usage} / {max_disk} GB.')
    count += 1
    print(f'You have download {count} of {max_video}.')
    
    os.remove(video_temp)
    os.remove(audio_temp)
    
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
                    video_path = r"{0}/video_output/".format(path)
                    print(r"Downloading Video with Audio: {0}.mp4".format(link.title))
                    pytube.YouTube(video, on_progress_callback=on_progress).streams.get_by_itag(tag.itag).download(output_path=video_path, max_retries=500, skip_existing=True)
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
