"""
Read and write title, artist, album and their sort orders.
"""

from mutagen.aiff import AIFF
from mutagen.mp4 import MP4
from mutagen.flac import FLAC
from mutagen.id3 import ID3FileType, TextFrame
from mutagen import id3
from typing import Iterable

SUPPORTED_EXTENTIONS = {".aiff", ".m4a", ".mp3", ".flac"}

def filter_extensions(filenames: Iterable[str]) -> Iterable[str]:
    for i in filenames:
        lwr = i.lower()
        for j in SUPPORTED_EXTENTIONS:
            if lwr.endswith(j):
                yield i
                break


class MusicTag:

    def __init__(self, filename: str):
        fn_lwr = filename.lower()

        if fn_lwr.endswith('aiff'):
            parser = AIFF
            self.factory = id3
            self.title_tag = 'TIT2'
            self.artist_tag = 'TPE1'
            self.album_tag = 'TALB'
            self.title_sort_tag = 'TSOT'
            self.album_sort_tag = 'TSOA'
            self.artist_sort_tag = 'TSOP'
        elif fn_lwr.endswith('m4a'):
            parser = MP4
            self.factory = None
            self.title_tag = '\xa9nam'
            self.artist_tag = '\xa9ART'
            self.album_tag = '\xa9alb'
            self.title_sort_tag = 'sonm'
            self.album_sort_tag = 'soal'
            self.artist_sort_tag = 'soar'
        elif fn_lwr.endswith('mp3'):
            parser = ID3FileType
            self.factory = id3
            self.title_tag = 'TIT2'
            self.artist_tag = 'TPE1'
            self.album_tag = 'TALB'
            self.title_sort_tag = 'TSOT'
            self.album_sort_tag = 'TSOA'
            self.artist_sort_tag = 'TSOP'
        elif fn_lwr.endswith("flac"):
            arser = FLAC
            self.factory = None
            self.title_tag = 'TITLE'
            self.artist_tag = 'ARTIST'
            self.album_tag = 'ALBUM'
            self.title_sort_tag = 'TITLESORT'
            self.album_sort_tag = 'ALBUMSORT'
            self.artist_sort_tag = 'ARTISTSORT'
        else:
            raise NotImplementedError(f"{filename} is in a not supported file type.")

        # self.file = open(filename, 'wb')

        self.parser = parser(filename)

        self.title = self.get_tag_text(self.parser, self.title_tag)
        self.artist = self.get_tag_text(self.parser, self.artist_tag)
        self.album = self.get_tag_text(self.parser, self.album_tag)

        self.title_sort = self.get_tag_text(self.parser, self.title_sort_tag)
        self.artist_sort = self.get_tag_text(self.parser, self.artist_sort_tag)
        self.album_sort = self.get_tag_text(self.parser, self.album_sort_tag)

    @staticmethod
    def get_tag_text(parser, tag_name) -> str:
        tag = parser.tags.get(tag_name, None)
        if tag is None:
            return ''
        if isinstance(tag, TextFrame):
            return ''.join(tag.text)
        elif isinstance(tag, list):
            return ''.join(tag)
        raise TypeError(f"Unknown type: {type(tag)} ({tag})")

    def set_tag_text(self, tag_name, value):
        if self.factory is id3:
            if tag_name in self.parser.tags:
                self.parser.tags[tag_name].text = [value]
                self.parser.tags[tag_name].encoding = id3.Encoding.UTF8
            else:
                cls = getattr(id3, tag_name)
                frame = cls(encoding=id3.Encoding.UTF8, text=[value])
                self.parser.tags[tag_name] = frame
        else:
            self.parser.tags[tag_name] = [value]

    def save(self):
        self.set_tag_text(self.title_tag, self.title)
        self.set_tag_text(self.artist_tag, self.artist)
        self.set_tag_text(self.album_tag, self.album)

        self.set_tag_text(self.title_sort_tag, self.title_sort)
        self.set_tag_text(self.artist_sort_tag, self.artist_sort)
        self.set_tag_text(self.album_sort_tag, self.album_sort)

        self.parser.save()
