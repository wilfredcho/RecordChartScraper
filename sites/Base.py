from abc import ABC, abstractmethod


class Base(ABC):

    @abstractmethod
    def proc_row(self, row, chart):
        pass

    @abstractmethod
    def run(self, soup, chart):
        pass
