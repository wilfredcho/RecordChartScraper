import re

from fuzzywuzzy import fuzz
from nltk import word_tokenize

import sites.common.compare as compare
from sites.common.constants import MATCH_RATIO
from sites.common.Info import Info


def condit(info, chart):
    
    return all([getattr(compare, condit)(info, val)
                for condit, val in chart.condit.items() if val]) and \
                not bool(set(word_tokenize(info.title.lower())).intersection(set(chart.dislike_title))) and \
                not any(dislike_artist.lower() in info.artist.lower()
                        for dislike_artist in chart.dislike_artist)


def format_text(text):
    if text:
        try:
            value = int(re.sub(r'\s+', '', text))
        except ValueError:
            value = re.sub(r'\s+', ' ', text)
        return value


def proc_info(chart, cur_pos, last_pos, title, artist):
        info = Info(cur_pos, last_pos, title, artist)
        for song in chart.old_songs:
            if fuzzy_match(info.artist + info.title, song[0] + song[1]):
                return
        if condit(info, chart):
            return (artist, title)


def alpha_only(text):
    return ''.join(char.lower()
                   for char in text if char.isalpha() or char == ' ')


def fuzzy_match(text1, text2):
    return fuzz.ratio(alpha_only(text1), alpha_only(text2)) > MATCH_RATIO


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
