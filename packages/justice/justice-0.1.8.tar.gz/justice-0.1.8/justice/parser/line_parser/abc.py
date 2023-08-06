import abc
import dateparser


class AbstractLineParser:
    def parse(self, data):
        parsed_date = None
        parsed_data = self.parse_data(data[0])
        if len(data) > 1:
            parsed_date = self.parse_date(data[1])
        return parsed_data, parsed_date

    @abc.abstractmethod
    def parse_data(self, data):
        pass

    @staticmethod
    def parse_date(data: str):
        result = {}
        expire = data.split('\n')
        expire_from = expire[0].replace('zapsáno\xa0', '')
        result['valid_from'] = dateparser.parse(expire_from)
        if len(expire) == 2:
            expire_to = expire[1].replace('vymazáno\xa0', '')
            result['valid_to'] = dateparser.parse(expire_to)
        return result
