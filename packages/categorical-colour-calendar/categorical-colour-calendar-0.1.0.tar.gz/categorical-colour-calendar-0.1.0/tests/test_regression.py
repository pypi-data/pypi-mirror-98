import pandas as pd
from matplotlib.testing.decorators import image_comparison

from cccalendar import draw_colour_calendar


@image_comparison(baseline_images=['line_dashes'], extensions=['png'], savefig_kwarg={'bbox_inches': 'tight'})
def test_simple_calendar():
    s = pd.Series({'2021-01-01': 'a'})
    cm = {'a': 'r'}
    draw_colour_calendar(s, cm)
