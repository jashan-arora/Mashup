import os
import moviepy.editor as mp
from pytube import Search, YouTube
import googleapiclient.discovery
import re
import ssl
import concurrent.futures
ssl._create_default_https_context = ssl._create_stdlib_context


def Download_Task(url, index, singer):
    song = YouTube(url)
    stream = song.streams.get_lowest_resolution()
    stream.download(output_path='media/Downloader/videos/'+singer, filename=str(index)+'.mp4',
                    filename_prefix='Song_')


def get_song_links(singer, n):

    api_key = os.environ.get('YOUTUBE_API_KEY')
    youtube = googleapiclient.discovery.build(
        'youtube', 'v3', developerKey='AIzaSyBqh1AlprgXDqPe80NzT0J8Higuy6xPi90')

    request = youtube.search().list(
        part='id',
        type='video',
        q=singer + ' Songs',
        videoDuration='short',
        pageToken=None,
        maxResults=n
    )

    links = []

    while len(links) < n:
        response = request.execute()

        for item in response['items']:
            links.append('https://www.youtube.com/watch?v=' +
                         item['id']['videoId'])

        next_page_token = response.get('nextPageToken', None)

        if next_page_token is None or len(links) >= n:
            break

        request = youtube.search().list(
            part='id',
            type='video',
            q='search_query',
            maxResults=50,
            pageToken=next_page_token
        )

    data = [(element, index + 1, singer)
            for index, element in enumerate(links[:n])]

    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        results = list(executor.map(lambda x: Download_Task(*x), data))


def DownloadThread(singer, count):
    search = Search(singer+" Songs")
    match = ".*"+singer.lower()+".*"
    final_list = []
    start = 0
    while(len(final_list) < count):
        song_list = search.results
        end = len(song_list)
        for index in range(start, end):
            song = song_list[index]
            if(re.search(match, song.title.lower()) and song.length < 360):
                final_list.append(song)
            if(len(final_list) == count):
                break
        search.get_next_results()
        start = end

    data = [(element, index + 1, singer)
            for index, element in enumerate(final_list)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        results = list(executor.map(lambda x: Download_Task(*x), data))


def Convert_To_Audio(singer, x, y):
    for i in range(1, x+1):
        name = "Song_"+str(i)
        clip = mp.VideoFileClip(
            'media/Downloader/videos/'+singer+'/'+name+'.mp4')
        if not os.path.exists('media/Downloader/audios/'+singer):
            os.mkdir('media/Downloader/audios/'+singer)
        trimmed = clip.subclip(0, y)
        trimmed.audio.write_audiofile(
            'media/Downloader/audios/'+singer+'/'+name+'.mp3')


def Merge_Audios(singer, x):
    clip = []
    for i in range(1, x+1):
        name = "Song_"+str(i)
        clip.append(mp.AudioFileClip(
            'media/Downloader/audios/'+singer+'/'+name+'.mp3'))
    merged_audio = mp.concatenate_audioclips(clip)
    merged_audio.write_audiofile(
        'media/Downloader/audios/'+singer+'/'+'Merged_'+singer+'.mp3')


def Download(singer, x=3):
    search = Search(singer+" Songs")
    match = ".*"+singer.lower()+".*"
    final_list = []
    start = 0
    while(count < x):
        song_list = search.results
        end = len(song_list)-start
        for index in range(start, end):
            song = song_list[index]
            if(re.search(match, song.title.lower()) and song.length < 360):
                count = count+1
                stream = song.streams.get_by_itag(22)
                stream.download(output_path='media/Downloader/videos/'+singer, filename=str(count)+'.mp4',
                                filename_prefix='Song_')
            if count == x:
                break
        search.get_next_results()
        start = end


singer = "Arijit Singh"

DownloadThread(singer, 50)

# Convert_To_Audio(singer, 20, 20)

# Merge_Audios(singer, 20)
