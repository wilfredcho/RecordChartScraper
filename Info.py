class Info(object):

    def __init__(self, cur_pos, last_pos, title, artist):
        self.cur_pos = int(cur_pos)
        if last_pos == 'New':
           self.last_pos = 1000 
        elif last_pos == 'Re':
            self.last_pos = -1 
        else:
            self.last_pos = int(last_pos)
        self.title = title
        self.artist = artist
