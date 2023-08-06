import re
from datetime import datetime

import pandas as pd

from colourutils import get_n_colours, extend_colour_map

colour_regex = '#[a-fA-F0-9]{6}'

# https://matplotlib.org/gallery/color/named_colors.html
colours = [
    'w',  # base colors
    'tab:red',  # tableau palette
    'lime',  # css colors
    'xkcd:azure',  # xkcd colors
    (59 / 255, 22 / 255, 23 / 255),  # rgb
    '#f284ff',  # hex
    (255 / 255, 0 / 255, 255 / 255, 0.3),  # rgba
]

hex_output_expectation = {'w': '#ffffff', 'tab:red': '#d62728', 'lime': '#00ff00', 'xkcd:azure': '#069af3',
                          (0.23137254901960785, 0.08627450980392157, 0.09019607843137255): '#3b1617',
                          '#f284ff': '#f284ff',
                          (1.0, 0.0, 1.0, 0.3): '#ff00ff'}


def test_get_n_colours():
    for n in range(10):
        assert len(get_n_colours(n)) == n


def test_extend_colour_map():
    colour_map = {f'event_{i}': colours[i] for i in range(len(colours))}
    dates = pd.date_range(start='2021-01-01', periods=len(colour_map), freq='2D')
    s = pd.Series(colour_map.keys(), index=dates)
    s[datetime(2021, 1, 15)] = 'event_7'
    s[datetime(2021, 1, 17)] = 'event_8'

    new_colour_map, new_date_colour = extend_colour_map(s, colour_map, None)
    original_to_converted = {orig_col: new_colour_map[ev] for ev, orig_col in colour_map.items()}

    assert len(new_colour_map) == len(s)  # Every event has a mapped colour
    assert all([re.match(colour_regex, c) for c in new_colour_map.values()])  # All colours are hex format
    assert all([e in new_colour_map for e in ['event_7', 'event_8']])  # Colours generated for unmapped events
    assert new_date_colour is not None  # New colour generated for date colour
    assert original_to_converted == hex_output_expectation  # Values in provided colour map correctly converted to hex
    assert len(set(new_colour_map.values())) == len(new_colour_map)  # Assert colours are unique


def test_extend_colour_map_no_new_date_colour():
    colour_map = {f'event_{i}': colours[i] for i in range(len(colours))}
    dates = pd.date_range(start='2021-01-01', periods=len(colour_map), freq='2D')
    s = pd.Series(colour_map.keys(), index=dates)
    s[datetime(2021, 1, 15)] = 'event_7'
    s[datetime(2021, 1, 17)] = 'event_8'

    new_colour_map, new_date_colour = extend_colour_map(s, colour_map, date_colour='black')
    original_to_converted = {orig_col: new_colour_map[ev] for ev, orig_col in colour_map.items()}

    assert len(new_colour_map) == len(s)  # Every event has a mapped colour
    assert all([re.match(colour_regex, c) for c in new_colour_map.values()])  # All colours are hex format
    assert all([e in new_colour_map for e in ['event_7', 'event_8']])  # Colours generated for unmapped events
    assert new_date_colour == '#000000'  # Date colour (black) is converted to hex
    assert original_to_converted == hex_output_expectation  # Values in provided colour map correctly converted to hex
