import http
import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.id = self.get_all("", "id")["id"]
        self.title = self.get_all("snippet", "title")["title"]
        self.description = self.get_all("snippet", "description")["description"]
        self.url = "https://www.youtube.com/channel/" + self.__channel_id
        self.subscriber_count = self.get_all("statistics", "subscriberCount")["subscriberCount"]
        self.video_count = self.get_all("statistics", "videoCount")["videoCount"]
        self.view_count = self.get_all("statistics", "viewCount")["viewCount"]

    info = {}
    api_key: str = os.getenv('YT_API_KEY')

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        dict_to_print = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        json.dumps(dict_to_print, indent=2, ensure_ascii=False)

    def get_all(self, word1, word2):
        """Заполняет словарь self.info значениячми для полей класса Channel."""
        # api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        dict_to_print = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        if word1 == "":
            self.info[word2] = dict_to_print["items"][0][word2]
        else:
            self.info[word2] = dict_to_print["items"][0][word1][word2]
        return self.info

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, filename):
        with open(filename, "w") as write_file:
            my_string = json.dumps(self.info, ensure_ascii=False).encode('utf-8').decode()
            json.dump(my_string, write_file, ensure_ascii=False)

    def __str__(self):
        """
        Возвращает название и ссылку на канал.
        """
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        """
        Складывет количество подписчиков двух каналов между собой.
        """
        if not isinstance(other, Channel):
            return NotImplemented
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        """
        Вычитает количество подписчиков каналов.
        """
        if not isinstance(other, Channel):
            return NotImplemented
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        """
        Сравнивает количество подписчиков канала self и канала other (больше).
        """
        if not isinstance(other, Channel):
            return NotImplemented
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        """
        Сравнивает количество подписчиков канала self и канала other (больше или равно).
        """
        if not isinstance(other, Channel):
            return NotImplemented
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other):
        """
        Сравнивает количество подписчиков канала self и канала other (меньше).
        """
        if not isinstance(other, Channel):
            return NotImplemented
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        """
        Сравнивает количество подписчиков канала self и канала other (меньше или равно).
        """
        if not isinstance(other, Channel):
            return NotImplemented
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other):
        """
        Сравнивает количество подписчиков канала self и канала other.
        """
        if not isinstance(other, Channel):
            return NotImplemented
        return int(self.subscriber_count) == int(other.subscriber_count)
