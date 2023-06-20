import os

from googleapiclient.discovery import build


class Video:
    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, video_id: str):
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.video_id = video_id  # gaoc9MPZ4bw
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.video_id
                                               ).execute()
        try:
            self.title: str = video_response['items'][0]['snippet']['title']
        except IndexError:
            self.title = None
        try:
            self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        except IndexError:
            self.view_count = None
        try:
            self.like_count: int = video_response['items'][0]['statistics']['likeCount']
        except IndexError:
            self.like_count = None
            self.url = None
        else:
            self.url = "https://www.youtube.com/watch?v=" + self.video_id

    def __str__(self):
        """
        Возвращает название видео.
        """
        return self.video_title


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id
