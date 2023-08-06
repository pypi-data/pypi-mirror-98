from . import AbstractLineParser


class EmptyLineParser(AbstractLineParser):
    def parse_data(self, data):
        pass

    @staticmethod
    def parse_date(data: str):
        pass
