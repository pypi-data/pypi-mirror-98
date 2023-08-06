import pandas as pd
from cccalendar import draw_colour_calendar

s = pd.Series({
    '2019-04-22': 'Summer Term start',
    '2019-05-20': 'Half Term',
    '2019-05-21': 'Half Term',
    '2019-05-22': 'Half Term',
    '2019-05-23': 'Half Term',
    '2019-05-24': 'Half Term',
    '2019-05-31': 'Inset Day',
    '2019-07-19': 'Summer Term end',
    '2019-05-13': 'A Levels start',
    '2019-06-26': 'A Levels end',
    '2019-07-29': 'Staff Training Day'
})
s2 = pd.Series({
    '2019-05-13': 'GCSE start',
    '2019-06-21': 'GCSE end',
})
s = s.append(s2)
draw_colour_calendar(s,
                     months_per_row=2,
                     min_date='2019-04-22',
                     max_date='2019-07-19')
