def find_high_resolution(link):
    if link.streams.filter().get_by_itag(137) != None:
        print('Find: 1080p')
        return link.streams.filter().get_by_itag(137)
    elif link.streams.filter(progressive=True).get_by_resolution("720p") != None:
        print('Find: 720p')
        return link.streams.filter(progressive=True).get_by_resolution("720p")
    elif link.streams.filter(progressive=True).get_by_resolution("480p") != None:
        print('Find: 480p')
        return link.streams.filter(progressive=True).get_by_resolution("480p")
    elif link.streams.filter(progressive=True).get_by_resolution("360p") != None:
        print('Find: 360p')
        return link.streams.filter(progressive=True).get_by_resolution("360p")
    elif link.streams.filter(progressive=True).get_by_resolution("144p") != None:
        print('Find: 144p')
        return link.streams.filter(progressive=True).get_by_resolution("144p")
    else:
        return None
