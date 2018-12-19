import sites.common.compare as compare
import re
from fuzzywuzzy import fuzz
from sites.common.Info import Info
from sites.common.constants import MATCH_RATIO


def condit(info, chart):
    return all([getattr(compare, condit)(info, val)
                for condit, val in chart.condit.items() if val]) and \
        not any(title.lower() in info.title.lower() for title in chart.dislike_title) and \
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
    if condit(info, chart):
        return (artist, title)


def alpha_only(text):
    return ''.join(char for char in text if char.isalpha() or char == ' ')


def fuzzy_match(text1, text2):
    return fuzz.ratio(alpha_only(text1), alpha_only(text2)) > MATCH_RATIO
