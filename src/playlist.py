import datetime
import os

import isodate
from googleapiclient.discovery import build
import requests
from src.channel import Channel
from src.video import PLVideo, Video


class PlayList(PLVideo):
    datetime.timedelta

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        #  super().__init__(playlist_id)
        self.title = self.find_title()
        self.url = "https://www.youtube.com/playlist?list=" + self.playlist_id
        # self.__total_duration = datetime.timedelta(seconds=0)

    def find_title(self):
        url1 = "https://www.googleapis.com/youtube/v3/playlists?key=" + self.api_key
        url2 = "&id=" + self.playlist_id + "&part=id,snippet&fields=items(id,snippet(title,channelId,channelTitle))"
        url = url1 + url2
        response = requests.get(url)
        return response.json()["items"][0]["snippet"]["title"]

    def duration(self):
        times = []
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        for i in range(len(video_response["items"])):
            times.append(isodate.parse_duration(video_response["items"][i]["contentDetails"]["duration"]))

        return times

    @property
    def total_duration(self):
        return datetime.timedelta(seconds=sum(td.total_seconds() for td in self.duration()))

    def show_best_video(self):
        like_count = {}
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        for i in range(len(video_response["items"])):
            like_count[video_response["items"][i]["id"]] = video_response["items"][i]["statistics"]["likeCount"]
        max_v = max(like_count, key=like_count.get)
        return "https://youtu.be/" + max_v




