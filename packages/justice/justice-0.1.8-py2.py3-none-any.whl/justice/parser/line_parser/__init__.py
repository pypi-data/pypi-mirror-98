from justice.parser.line_parser.abc import AbstractLineParser
from justice.parser.line_parser.company_name import CompanyNameParser
from justice.parser.line_parser.empty import EmptyLineParser

detail_parser_mapping = {
    'Obchodní firma:': CompanyNameParser,
    'Sídlo:': EmptyLineParser,
}


__all__ = (
    'AbstractLineParser',
    'CompanyNameParser',
    'EmptyLineParser',

    'detail_parser_mapping',
)
