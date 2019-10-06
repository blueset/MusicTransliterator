import requests
import xml.etree.ElementTree as ET

from abc import ABC, abstractclassmethod
from pypinyin import pinyin


class Transliterator(ABC):

    @classmethod
    @abstractclassmethod
    def transiterate(cls, text: str) -> str:
        """Transliterate a text"""
        return text


class PinyinTransliterator(Transliterator):
    @classmethod
    def transiterate(cls, text: str) -> str:
        return ''.join(i[0] for i in pinyin(text))


class HiraganaTransliterator(Transliterator):
    @classmethod
    def set_app_id(cls, app_id: str):
        cls.app_id = app_id

    @classmethod
    def transiterate(cls, text: str) -> str:
        resp = requests.get(
            "https://jlp.yahooapis.jp/MAService/V1/parse",
            params={
                "appid": cls.app_id,
                "sentence": text,
                "results": "ma"
            }
        )
        root = ET.fromstring(resp.text)
        result = ''.join(i.text for i in root.findall('.//{urn:yahoo:jp:jlp}reading'))
        result = "".join([chr(ord(ch) - 96) if ("ァ" <= ch <= "ヴ") else ch for ch in result])
        return result
