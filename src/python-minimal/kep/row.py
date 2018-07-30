from collections import namedtuple
import kep.filters as filters

ROW_FORMAT_DICT = {len(x): x for x in [
    'YAQQQQMMMMMMMMMMMM',
    'YAQQQQ',
    'YAMMMMMMMMMMMM',
    'YMMMMMMMMMMMM',
    'YQQQQ',
    'XXXX']}

Datapoint = namedtuple('Datapoint', 'label freq year month value')    


def get_format(row_length: int, row_format_dict=ROW_FORMAT_DICT):
    try:
        return row_format_dict[row_length]
    except KeyError:
        raise ValueError(f'Cannot decide on row format: {row_length}')
    

def get_month(freq: str, period: int):
    if freq == 'a':
        return 12
    elif freq == 'q':
        return period * 3
    return period


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
                                #FIXME: maybe should clean year too 
                                int(year),
                                get_month(freq, period), 
                                filters.clean_value(value))

# WONTFIX
# must fail on row
#['до/up to 2000,0', '2,6', '1,5', '1,0']
