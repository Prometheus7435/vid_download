'''
script to download vidoes and add metadata to it.
'''

import os
import sys
import time
#import youtube_dl
from youtube_dl import YoutubeDL
from urllib.request import urlopen
import urllib
import requests
from multiprocessing import Pool
#import mutagen
#from mutagen.mp4 import MP4


"""
mutagen notes to self


from stackoverflow
I'm currently using the Mutagen module for Python to prepare the MP4 Tags of a video-file for iTunes. It works fine, but I miss one really important tag, it's called "stik" and stands for the iTunes media type.

This is my current code:

mp4_video_tags = MP4(mp4_file)

mp4_video_tags['\xa9nam'] = 'Video Name'
mp4_video_tags['\xa9alb'] = 'DVD-Name'
mp4_video_tags['\xa9gen'] = 'Video-Training'
mp4_video_tags['\xa9day'] = '2015'
mp4_video_tags['\xa9ART'] = 'Company'
mp4_video_tags['aART'] = 'Company'
mp4_video_tags['\xa9wrt'] = 'Company'
mp4_video_tags['cprt'] = 'Copyright (c) Company'
mp4_video_tags['desc'] = 'description'
mp4_video_tags['tvsh'] = 'DVD-Name'
mp4_video_tags['trkn'] = [(1, 18)]
mp4_video_tags['disk'] = [(1, 1)]
mp4_video_tags['stik'] = 10

mp4_video_tags.save()
"""


class Downloader:

    def __init__(self):
        self.fsave = os.path.abspath(r"/home/zach/Videos/")
        os.chdir(self.fsave)

    def askSite(self, videos):
        if 'animefreak.tv' in videos:
            animeFreak(videos)
        elif 'thewatchcartoononline.tv' in videos:
            watchCartoon(videos)
        else:
            with Pool(2) as p:
                p.map(download, videos)

    
def download(options, opts=''):
    '''
    param site: site that you want to download
    param opts: youtube-dl download options
    '''
    site = options[0]
    # print(site)
    os.chdir(options[1])
#    ydl_opts = {'format':'bestvideo+bestaudio/best'}
#    try:
#    ydl_opts = {"format":"best[height <= 2048]"}
#    except Exception as e:
    ydl_opts = { 'quiet': True,
                 'no_warnings': True}
    with YoutubeDL(ydl_opts) as ydl:
#        result = ydl.extract_info([site], download=False)
        ydl.download([site])
#    mp4_video_tags = MP4(mp4_file)

#    mp4_video_tags['\xa9nam'] = 'Video Name'
#    mp4_video_tags['\xa9alb'] = 'DVD-Name'
#    mp4_video_tags['\xa9gen'] = 'Video-Training'
#    mp4_video_tags['\xa9day'] = '2015'
#    mp4_video_tags['\xa9ART'] = 'Company'
#    mp4_video_tags['aART'] = 'Company'
#    mp4_video_tags['\xa9wrt'] = 'Company'
#    mp4_video_tags['cprt'] = 'Copyright (c) Company'
#    mp4_video_tags['desc'] = 'description'
#    mp4_video_tags['tvsh'] = 'DVD-Name'
#    mp4_video_tags['trkn'] = [(1, 18)]
#    mp4_video_tags['disk'] = [(1, 1)]
#    mp4_video_tags['stik'] = 10

#    mp4_video_tags.save()


def save_folder(series_save):
    try:
        os.mkdir(series_save)
        os.mkdir(os.path.join(series_save, "tmp"))
    except:
        pass
        # s_save = os.path.join(fsave, series)
    s_save = os.path.join(series_save, "tmp")

    return s_save

def animeFreak(site, fsave):
    ep = []
    
    series = site.split('animefreak.tv/watch/')[1]
    gstr = 'href="https://www.animefreak.tv/home/genres/'    
    # print(series)
    series_save = os.path.join(fsave, series)
    s_save = save_folder(series_save)
    os.chdir(s_save)    


    # html = urlopen(str(site)).read().decode('utf-8')
            
    genre = []
    # numEp = input(str("How many episodes does ", series, " have?\n>"))
    req = urllib.request.Request(site, headers={'User-Agent': 'Mozilla/5.0'})
    infodump = urlopen(req).read().decode('utf-8')

    # print(site)
    
    episodecount = []
    sets = infodump.split('<')
    for i, s in enumerate(sets):
        if 'href="https://www.animefreak.tv/home/genres/' in s:
            genre.append(s.split('href="https://www.animefreak.tv/home/genres/')[1].split('"')[0])
        if str('href="' + site + '/episode/episode-') in s:
            episodecount.append(s.split(str('href="' + site + '/episode/episode-'))[1].split('"')[0])
            # href="https://www.animefreak.tv/watch/shin-chuuka-ichiban/episode/episode-8"
        if '>Season :' in s:
            print(sets[i+2].split('href="https://www.animefreak.tv/home/')[1].split('"')[0])

    # print(episodecount)
            
    # genre = infodump.split(gstr)[1].split('">')[0]
    # # genre = urlopen(req).read().decode().split(gstr)[1].split('">')[0]    
    # synop = infodump.split('class="anime-details">')[1].split('<')[0]
    # # print(synop)

    # # print(episodes)
    ep_count = int(max(episodecount))
    # print(ep_count)

    
    ep = [[str(site + '/episode/episode-' + str(n)), s_save] for n in range(1,(ep_count  + 1))]
    # print(genre)
    out_genre = ""
    for g in genre:
        tmp = ""
        tmp = str(out_genre + "," + g)
        out_genre = tmp
    out_genre = out_genre[1:]
    # # print(out_genre)
    # # download(ep[-2])
    try:
        with Pool(3) as p:
            p.map(download, ep)
    except Exception as e:
        print(e)

    # # print(genre, series, s_save)
    sys.stdout.write("{} {} {}".format(out_genre, series, s_save))
    return out_genre, series, s_save, ep_count

def watchCartoon(site):
    numEp = 1000
    genre = []
    ep = []
    start = 'https://www.thewatchcartoononline.tv/'
    fullseries = site.split('thewatchcartoononline.tv/anime/')[1]
    # dub = ''
    # if fullseries.endswith('-dubbed-episodes'):
    #     dub = '-english-dubbed'
    # elif fullseries.endswith('-subbed-episodes'):
    #     dub = '-english-subbed'
    # else:
    #     dub = False

    # print(site)
    # print(fullseries)
    try:
        series = site.split('thewatchcartoononline.tv/anime/')[1].split('-english')[0]
    except:
        series = site.split('thewatchcartoononline.tv/anime/')[1]
    # print("series:  " + str(series))

    # print(str('href="' + site + '-episode-'))
    # print(str('href="' + site.replace('anime/','')))
    # sys.exit()

    s_save = save_folder(series)


    
    genre = []
    # numEp = input(str("How many episodes does ", series, " have?\n>"))
    req = urllib.request.Request(site, headers={'User-Agent': 'Mozilla/5.0'})
    infodump = urlopen(req).read().decode('utf-8')

    episodecount = []
    sets = infodump.split('<')
    for i, s in enumerate(sets):
        # print(s)
        if '"genre-buton">' in s:
            genre.append(s.split('"genre-buton">')[1])
        if str('href="' + site.replace('anime/','').replace('ova', '')) in s:
            # print(s.split(str(site.replace('anime/','').replace('-ova', '') + '-episode-'))[1].split('-english')[0])
            episodecount.append(int(s.split(str(site.replace('anime/','').replace('-ova', '') + '-episode-'))[1].split('-english')[0]))
    #     if str('href="' + site + '/episode/episode-') in s:
    #         episodecount.append(s.split(str('href="' + site + '/episode/episode-'))[1].split('"')[0])
    #         # href="https://www.animefreak.tv/watch/shin-chuuka-ichiban/episode/episode-8"
    #     if '>Season :' in s:
    #         print(sets[i+2].split('href="https://www.animefreak.tv/home/')[1].split('"')[0])

    ep_count = int(max(episodecount))
    print(ep_count)
    ep = [[str(site + '/episode/episode-' + str(n)), s_save] for n in range(1,(ep_count  + 1))]

    out_genre = ""
    for g in genre:
        tmp = ""
        tmp = str(out_genre + "," + g)
        out_genre = tmp
    out_genre = out_genre[1:]
    # print(out_genre)


    
    # req = urllib.request.Request(site, headers={'User-Agent': 'Mozilla/5.0'})
    # gen = urlopen(req).read().decode().split('</')
        
    # for g in gen:
    #     if 'class="genre-buton">' in g:
    #         genr = g.split('class="genre-buton">')[1]
    #         genre.append(genr)
    # for n in range(int(numEp)):
    #     ep.append(str(start + series.split(dub)[0] + '-episode-' + str(n+1) + dub))


    download(ep[-2])
    # try:
    #     with Pool(3) as p:
    #         p.map(download, ep)
    # except Exception as e:
    #     print(e)

    
    sys.stdout.write("{} {} {}".format(out_genre, series, s_save))
    
def askSite(videos, fsave):
#    for s in site:
    if 'animefreak.tv' in videos:
        animeFreak(videos, fsave)
    elif 'thewatchcartoononline.tv' in videos:
        watchCartoon(videos)
    else:
#            for v in site:
#            html = uro(str(s)).read().decode('utf-8')
        with Pool(2) as p:
            p.map(download, videos)
#        download(s, ydl_opts)
                #        download(site)
    
        
if (__name__ == '__main__'):
    # fsave = input("Where do you want to save these to?\n>>")
    fsave = os.path.abspath(r"/home/zach/Videos/")
    os.chdir(fsave)
    
    videos = sys.argv[1]
    # videos = input()
    # videos = 'https://www.thewatchcartoononline.tv/anime/mobile-suit-gundam-wing'
    # videos = 'https://www.thewatchcartoononline.tv/anime/3-nen-d-gumi-glass-no-kamen-subbed-episodes'
    # videos = 'https://www.animefreak.tv/watch/one-piece'
    
    askSite(videos, fsave)

    
    # videos = str(input("Paste site url. For multiple, seperate with a space. Ex. video1 video2\n>>")).split(" ")    
#    ydl_opts = input("what options would you like?\n>>")
#    ydl_opts = {}


#    with Pool(3) as p:
#        p.map(askSite, videos)

