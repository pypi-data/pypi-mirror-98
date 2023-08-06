"""Main module."""
from pyquery import PyQuery as pq

from .parser import Parser


class Justice:
    SEARCH_URL = 'https://or.justice.cz/ias/ui/rejstrik?p::submit=x&\
-1.IFormSubmitListener-htmlContainer-top-form=&search={}'
    DETAIL_URL = 'https://or.justice.cz/ias/ui/rejstrik-firma.vysledky?subjektId={}&typ={}'
    DETAIL_TYPE_MAPPING = {'FULL': 'UPLNY', 'VALID': 'PLATNY'}

    def __init__(self, *, search_url=SEARCH_URL, detail_url=DETAIL_URL):
        self.SEARCH_URL = search_url
        self.DETAIL_URL = detail_url

    @classmethod
    def search(cls, string: str):
        doc = pq(url=cls.SEARCH_URL.format(string))
        return Parser.parse_list_result(doc)

    @classmethod
    def get_detail(cls, subject_id: str, typ: str = "FULL"):
        """
        :param subject_id: ID of subject
        :param typ: FULL/VALID
        :return:
        """
        assert typ in cls.DETAIL_TYPE_MAPPING, f"""`typ` has to be one of {[cls.DETAIL_TYPE_MAPPING.keys()]}.
        Not {typ}"""
        assert type(subject_id) == str, f"""`subject_id` has to be string, not {type(subject_id)}"""

        doc = pq(url=cls.DETAIL_URL.format(subject_id, cls.DETAIL_TYPE_MAPPING[typ]))
        return Parser.parse_detail_result(doc)


if __name__ == '__main__':
    justice = Justice()
    # print(justice.search('08431116'))
    # print(justice.search('Seznam'))

    print(justice.get_detail('1060090'))
    print(justice.get_detail('676708'))
