#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib.parse import urlparse, parse_qs

from pyquery import PyQuery as pq

from justice.parser import line_parser


class Parser:
    @staticmethod
    def parse_list_result(docs: pq):
        result = []
        for doc in docs('li.result'):
            result.append(Parser.parse_list_one(doc))
        return result

    @staticmethod
    def parse_list_one(doc: pq):
        doc = pq(doc)
        keys = ('name', 'ico', 'file_number', 'registration_date', 'resistance')
        result = {}
        for pos, table_data in enumerate(doc.find('table tbody tr td')):
            result[keys[pos]] = pq(table_data).text()
        subject_id = ''
        for link in doc.find('.result-links li a'):
            href = link.attrib['href']
            parsed_href = urlparse(href)
            parsed_query = parse_qs(parsed_href.query)
            if 'subjektId' in parsed_query:
                subject_id, = parsed_query['subjektId']
                break
        if subject_id:
            result['subject_id'] = subject_id
        return result

    @staticmethod
    def parse_detail_result(doc: pq):
        result = []
        doc = pq(doc.find(".section-c .aunp-content .div-row"))
        for table_row in doc:
            line = []
            for div_cell in pq(table_row).find('.div-cell'):
                line.append(pq(div_cell).text())
            result.append(line)
        parsed_result = []
        parser = line_parser.EmptyLineParser
        parser_key = ''
        for line in result:
            key = line[0]
            if key in line_parser.detail_parser_mapping:
                parser_key = key
                parser = line_parser.detail_parser_mapping[key]
            if len(line) >= 2:
                value, expired = parser().parse(data=line[1:])
                if value:
                    parsed_result.append((parser_key, value, expired))
        return parsed_result
