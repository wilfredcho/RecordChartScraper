from abc


class Base(ABC):
    
    __metaclass__  = abc.ABCMeta

    @abc.abstractmethod
    def proc_row(self, row, chart):
    #return proc_info(chart, cur_pos, last_pos, title, artist)

    @abc.abstractmethod
    def run(self, soup, chart):
    #return [self.proc_row(row, chart) for row in rows if bool(self.proc_row(row, chart))]
