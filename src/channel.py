import http
import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.id = self.get_all()["id"]
        self.title = self.get_all()["title"]
        self.description = self.get_all()["description"]
        self.url = self.get_all()["url"]
        self.subscriber_count = self.get_all()["subscriberCount"]
        self.video_count = self.get_all()["videoCount"]
        self.view_count = self.get_all()["viewCount"]

    info = {}
    api_key: str = os.getenv('YT_API_KEY')
    @property
    def channel_id(self):
        return self.__channel_id

    # @channel_id.setter
    # def channel_id(self, new_ch):
    #     self.__channel_id = new_ch

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        dict_to_print = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        json.dumps(dict_to_print, indent=2, ensure_ascii=False)

    def get_all(self):
        """Заполняет словарь self.info значениячми для полей класса Channel."""
        #api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        dict_to_print = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.info["id"] = dict_to_print["items"][0]["id"]
        self.info["title"] = dict_to_print["items"][0]["snippet"]["title"]
        self.info["url"] = "https://www.youtube.com/channel/" + self.__channel_id
        self.info["description"] = dict_to_print["items"][0]["snippet"]["description"]
        self.info["subscriberCount"] = dict_to_print["items"][0]["statistics"]["subscriberCount"]
        self.info["videoCount"] = dict_to_print["items"][0]["statistics"]["videoCount"]
        self.info["viewCount"] = dict_to_print["items"][0]["statistics"]["viewCount"]
        return self.info
    @staticmethod
    def get_service():
        api_key: str = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)