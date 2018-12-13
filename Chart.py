import pandas

class Chart(object):

    def __init__(self,config):
        self.meta = self._load_config(config)

    def _load_config(self, config):
        self.css_cur_pos = config.css_cur_pos
        self.ccs_last_pos = config.ccs_last_pos
        


