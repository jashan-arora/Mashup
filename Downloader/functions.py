import zipfile
import os
import moviepy.editor as mp
from pytube import Search, YouTube
import googleapiclient.discovery
import re
import ssl
import concurrent.futures
from Mashup.settings import YOUTUBE_API_KEY

ssl._create_default_https_context = ssl._create_stdlib_context


def Download_Task(url, index, singer):
    song = YouTube(url)
    stream = song.streams.get_lowest_resolution()
    stream.download(output_path='media/Downloader/videos/'+singer, filename=str(index)+'.mp4',
                    filename_prefix='Song_')


def Get_Links(singer, count):
    api_key = YOUTUBE_API_KEY
    youtube = googleapiclient.discovery.build(
        'youtube', 'v3', developerKey=api_key)

    request = youtube.search().list(
        part='id',
        type='video',
        videoDefinition='standard',
        q=singer + ' Songs',
        videoDuration='short',
        pageToken=None,
        maxResults=count
    )

    links = []

    while len(links) < count:
        response = request.execute()

        for item in response['items']:
            links.append('https://www.youtube.com/watch?v=' +
                         item['id']['videoId'])

        next_page_token = response.get('nextPageToken', None)

        if next_page_token is None or len(links) >= count:
            break

        request = youtube.search().list(
            part='id',
            type='video',
            q='search_query',
            maxResults=50,
            pageToken=next_page_token
        )
    return links


def Download_Songs(singer, count):
    links = Get_Links(singer, count)
    data = [(element, index + 1, singer)
            for index, element in enumerate(links[:count])]

    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        results = list(executor.map(lambda x: Download_Task(*x), data))


def Convert_Trim_Task(singer, index, duration):
    name = "Song_"+str(index)
    clip = mp.VideoFileClip(
        'media/Downloader/videos/'+singer+'/'+name+'.mp4')
    trimmed = clip.subclip(0, duration)
    trimmed.audio.write_audiofile(
        'media/Downloader/audios/'+singer+'/'+name+'.mp3')


def Convert_To_Audio_Trim(singer, count, duration):
    if not os.path.exists('media/Downloader/audios/'+singer):
        os.mkdir('media/Downloader/audios/'+singer)
    data = [(singer, index+1, duration) for index in range(count)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        results = list(executor.map(lambda x: Convert_Trim_Task(*x), data))


def Merge_Audios(singer, count):
    clip = []
    for i in range(1, count+1):
        name = "Song_"+str(i)
        clip.append(mp.AudioFileClip(
            'media/Downloader/audios/'+singer+'/'+name+'.mp3'))
    merged_audio = mp.concatenate_audioclips(clip)
    merged_audio.write_audiofile(
        'media/Downloader/audios/'+singer+'/'+singer+' Mashup'+'.mp3')


def Audio_to_Zip(singer):
    audio_file_path = 'media/Downloader/audios/'+singer+'/'+singer+' Mashup'+'.mp3'
    zip_file_path = 'media/Downloader/zips/'+singer+' Mashup'+'.zip'
    with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
        zip_file.write(audio_file_path, os.path.basename(audio_file_path))
