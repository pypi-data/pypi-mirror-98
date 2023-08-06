import re
from camtono.parser.format import BaseFormatter


def format_query(query_ast):
    query = BigQueryFormatter().format(query_ast)
    query = clean_table_names(query=query)

    return query


def clean_table_names(query):
    return re.sub('("[\S]+\.[\S]+\.[\S]+")', replace_quotes, query)


def replace_quotes(m):
    return m.string[m.span()[0]:m.span()[1]].replace('"', '`')


class BigQueryFormatter(BaseFormatter):
    pass
