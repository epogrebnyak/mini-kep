import calendar
from collections import namedtuple
import kep.filters as filters

MONTHS = dict(a=12, q=3, m=1)
ROW_FORMAT_DICT = {len(x): x for x in [
    'YAQQQQMMMMMMMMMMMM',
    'YAQQQQ',
    'YAMMMMMMMMMMMM',
    'YMMMMMMMMMMMM',
    'YQQQQ',
    'XXXX']}

Datapoint = namedtuple('Datapoint', 'label freq date value')    


#FIXME: can supply format directly without fiscal

def raise_format(key: str):
    raise ValueError(f'Unknown row format: {key}')


def get_format(row_length: int, row_format_dict=ROW_FORMAT_DICT):
    try:
        return row_format_dict[row_length]
    except KeyError:
        raise_format(row_length)


def assign_format(key: str):
    if key == 'fiscal':
        return 'YA' + 'M' * 11
    else:
        raise_format(key)


def timestamp(freq: str, 
              year: str, 
              period: int):
    year = filters.clean_year(year)
    month = MONTHS[freq] * period
    day = calendar.monthrange(year, month)[1]
    return f'{year}-{str(month).zfill(2)}-{day}'


def emit_datapoints(row, label, row_format):
    occurences = ''
    for value, letter in zip(row, row_format):
        occurences += letter
        if letter == 'Y':
            year = value
        else:
            if filters.number_string(value):
                period = occurences.count(letter)
                freq = letter.lower()
                yield Datapoint(label, 
                                freq, 
                                timestamp(freq, year, period), 
                                filters.clean_value(value))

# WONTFIX
# must fail on row
#['до/up to 2000,0', '2,6', '1,5', '1,0']
