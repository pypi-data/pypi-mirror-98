from .abc import AbstractLineParser
from .empty import EmptyLineParser
from .company_name import CompanyNameParser

detail_parser_mapping = {
    'Obchodní firma:': CompanyNameParser,
    'Sídlo:': EmptyLineParser,
}


__all__ = (
    'AbstractLineParser',
    'EmptyLineParser',
    'CompanyNameParser',

    'detail_parser_mapping',
)
