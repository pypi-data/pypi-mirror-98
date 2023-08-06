import re
from datetime import date

import pandas as pd

from datautils import extend_data_range, apply_colour_map, colour_data
from test_colourutils import colour_regex


def test_extend_data_range():
    s = pd.Series({
        date(2021, 2, 27): 'a',
        date(2021, 3, 1): 'b'
    })

    s = extend_data_range(s)

    assert s.index.min() == date(2021, 2, 1)
    assert s.index.max() == date(2021, 3, 31)

    t = pd.Series({
        date(2021, 1, 1): 'a',
        date(2021, 1, 31): 'b'
    })

    t = extend_data_range(t)

    assert t.index.min() == date(2021, 1, 1)
    assert t.index.max() == date(2021, 1, 31)

    u = pd.Series({
        '2021-01-31': 'a',
        '2021-03-01': 'b',
        '2021-02-01': 'a',
        '2021-01-15': 'b'
    })
    u.index = pd.to_datetime(u.index)
    u = extend_data_range(u)
    assert pd.to_datetime(u.index.values[0]) == date(2021, 1, 1)
    assert pd.to_datetime(u.index.values[-1]) == date(2021, 3, 31)
    assert len(u.index) == 90  # 31 + 28 + 31



def test_apply_colour_map():
    data = pd.Series(index=pd.date_range(start='2021-02-01', end='2021-02-28', freq='D'), dtype='object')
    data['2021-02-01'] = 'a'
    data['2021-02-14'] = 'b'
    data['2021-02-28'] = 'c'

    colour_map = {'a': '#ff0000', 'b': '#00ff00', 'c': '#0000ff'}

    data = apply_colour_map(data, colour_map, '#000000', '#ffffff', '2021-02-05', '2021-02-25')

    assert data['2021-02-01'] == '#ff0000'
    assert data['2021-02-14'] == '#00ff00'
    assert data['2021-02-28'] == '#0000ff'

    assert data[('2021-02-02' <= data.index) & (data.index < '2021-02-05')].unique() == ['#ffffff']
    assert data[('2021-02-05' <= data.index) & (data.index <= '2021-02-25') & (data.index != '2021-02-14')].unique() == ['#000000']
    assert data[('2021-02-25' < data.index) & (data.index != '2021-02-28')].unique() == ['#ffffff']


def test_colour_data():
    data = pd.Series({
        date(2021, 2, 5): 'a',
        date(2021, 2, 15): 'b',
        date(2021, 2, 25): 'c',
        date(2021, 3, 5): 'a',
        date(2021, 3, 15): 'b',
        date(2021, 3, 25): 'c'
    })

    colour_map = {'a': '#ff0000', 'b': '#00ff00'}
    start_date = '2021-02-10'
    end_date = '2021-03-20'
    exclude_colour = 'tab:gray'

    # Check values are generated for the date colour and c
    cd1, cm1 = colour_data(data, colour_map, None, exclude_colour, start_date, end_date, generate_missing_colours=True, strict_exclude=False)
    assert cd1['2021-02-01'] == exclude_colour  # Out of range dates are applied with the exclude colour
    assert cd1['2021-02-05'] == '#ff0000'  # Strict exclude is False so 'a' should still be mapped
    assert cd1['2021-02-10'] != exclude_colour and re.match(colour_regex, cd1['2021-02-10'])  # Default colour has been generated for in-range date
    assert cd1['2021-02-24'] != cd1['2021-02-25'] and re.match(colour_regex, cd1['2021-02-25'])  # Date colour has been generated for 'c'
    assert len(cm1) == 3

    # Check values are generated for the date colour but not c
    cd2, cm2 = colour_data(data, colour_map, None, exclude_colour, start_date, end_date, generate_missing_colours=False, strict_exclude=False)
    assert cd2['2021-02-01'] == exclude_colour  # Out of range dates are applied with the exclude colour
    assert cd2['2021-02-05'] == '#ff0000'  # Strict exclude is False so 'a' should still be mapped
    assert cd2['2021-02-10'] != exclude_colour and re.match(colour_regex, cd2['2021-02-10'])  # Default colour has been generated for in-range date
    assert cd2['2021-02-24'] == cd2['2021-02-25']  # Date colour has *not* been generated for 'c'
    assert cm2 == colour_map

    # Check values are excluded
    cd3, cm3 = colour_data(data, colour_map, '#ffffff', exclude_colour, start_date, end_date, generate_missing_colours=False, strict_exclude=True)
    assert cd3['2021-02-01'] == exclude_colour  # Out of range dates are applied with the exclude colour
    assert cd3['2021-02-05'] == exclude_colour  # Strict exclude is True so 'a' should not be mapped
    assert cd3['2021-03-25'] == exclude_colour  # Strict exclude is True so 'c' should not be mapped
    assert cd3['2021-02-10'] != exclude_colour and re.match(colour_regex, cd3['2021-02-10'])  # Default colour has been generated for in-range date
    assert cd3['2021-03-05'] == '#ff0000'  # In-range 'a' should still be mapped
    assert cm3 == colour_map
