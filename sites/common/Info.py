import sites.common.constants as constants

class Info(object):

    def __init__(self, cur_pos, last_pos, title, artist):
        self.cur_pos = int(cur_pos)
        if isinstance(last_pos, str):
            if last_pos.lower() in constants.NEW:
                self.last_pos = 1000
            elif last_pos.lower() in constants.RE:
                self.last_pos = -1
            else:
                self.last_pos = 0
        else:
            self.last_pos = int(last_pos)
        self.title = str(title)
        self.artist = str(artist)
