import pandas as pd

def _quote_string(string: str):
    return '\'' + string + '\''
def _backtick_string(string: str):
    return '`' + string + '`'

def _list_like_string(string_list):    
    out = string_list
    if any(isinstance(s, str) for s in string_list):
        out = [_quote_string(str(i)) for i in string_list]
    else:
        out = [str(i) for i in out]
    out = '[' +  ', '.join(out) + ']'
    return out

def _make_filter(filter_list):
    data = 'data'
    or_filter = []
    for i in filter_list:
        and_filter = []
        for j in i:
            if isinstance(j[2], str):
                j = (j[0], j[1], _quote_string(j[2]))
            if isinstance(j[2], list):
                j = (j[0], j[1], _list_like_string(j[2]))
            and_filter.append(str(_backtick_string(j[0])) + ' ' + str(j[1]) + ' ' + str(j[2]))
        and_filter = ' and '.join(and_filter)
        or_filter.append('(' + and_filter + ')')
    query = ' or '.join(or_filter)
    return query


def filter(data, filter):
    return data.query(_make_filter(filter_list = filter))

def filter_query(data, filter_expression: str):
    return data.query(filter_expression)


def search(data, col_name:str, pattern: str):
    return data[data[col_name].astype('str').str.contains(pattern)]
