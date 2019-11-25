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

def download(site, opts=''):
    '''
    param site: site that you want to download
    param opts: youtube-dl download options
    '''
    print(site)
#    ydl_opts = {'format':'bestvideo+bestaudio/best'}
#    try:
#    ydl_opts = {"format":"best[height <= 2048]"}
#    except Exception as e:
    ydl_opts = {}
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


def animeFreak(site):

    series = site.split('animefreak.tv/watch/')[1]
    # print(series)

    # numEp = input(str("How many episodes does ", series, " have?\n>"))
    req = urllib.request.Request(site, headers={'User-Agent': 'Mozilla/5.0'})
    gstr = 'href="https://www.animefreak.tv/home/genres/'
    genre = urlopen(req).read().decode().split(gstr)[1].split('">')[0]

    ep = []
    for n in range(10): #int(numEp)):
        ep.append(str(site + '/episode/episode-' + str(n + 1)))

#     try:
#         with Pool(3) as p:
#             p.map(download, ep)
# #        for e in ep:
# #            download(e)
# #            time.sleep(20)
# #            print(e)
#     except Exception as e:
#         print(e)
    # sys.stdout.write(series + ' ' + genre)
    # sys.stdout.write(genre)
    print(genre, series)
    return genre, series

def watchCartoon(site):
    numEp = 1000
    genre = []
    ep = []
    start = 'https://www.thewatchcartoononline.tv/'
    fullseries = site.split('thewatchcartoononline.tv/anime/')[1]
    series = site.split('thewatchcartoononline.tv/anime/')[1].split('-english-dubbed')[0]
    print("series:  " + str(series))
    req = urllib.request.Request(site, headers={'User-Agent': 'Mozilla/5.0'})
    gen = urlopen(req).read().decode().split('</')
    dub = ''
    if '-english-dubbed' in fullseries:
        dub = '-english-dubbed'
    if '-english-subbed' in fullseries:
        dub = '-english-subbed'
        
    for g in gen:
        if 'class="genre-buton">' in g:
            genr = g.split('class="genre-buton">')[1]
            genre.append(genr)
    for n in range(int(numEp)):
        ep.append(str(start + series.split(dub)[0] + '-episode-' + str(n+1) + dub))
        
    try:
        with Pool(3) as p:
            p.map(download, ep)
    except Exception as e:
        print(e)
     
    
def askSite(videos):
#    for s in site:
    if 'animefreak.tv' in videos:
        animeFreak(videos)
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
    # videos = str(input("Paste site url. For multiple, seperate with a space. Ex. video1 video2\n>>")).split(" ")
    askSite(videos)    
#    ydl_opts = input("what options would you like?\n>>")
#    ydl_opts = {}


#    with Pool(3) as p:
#        p.map(askSite, videos)
