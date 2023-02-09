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


singer = 'Hardy Sandhu'
count = 5
get_song_links(singer, count)
