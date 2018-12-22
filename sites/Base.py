from abc


class Base(ABC):
    
    __metaclass__  = abc.ABCMeta

    @abc.abstractmethod
    def proc_row(self, row, chart):

    @abc.abstractmethod
    def run(self, soup, chart):
