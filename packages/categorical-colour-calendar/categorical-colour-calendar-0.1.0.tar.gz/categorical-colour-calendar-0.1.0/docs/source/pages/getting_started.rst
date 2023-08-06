##############################################
Getting Started
##############################################

Installation
#############
::

    pip install categorical-colour-calendar


Usage
#############
Basic
=======
Automatically generated colours
::

    import pandas as pd
    from cccalendar import draw_colour_calendar
    my_data = pd.Series({
        '2021-01-01': 'event_one',
        '2021-01-07': 'event_two',
        '2021-01-10': 'event_three',
        '2021-01-14': 'event_four',
        '2021-01-20': 'event_one',
        '2021-01-21': 'event_two',
    })
    draw_colour_calendar(my_data)

.. image:: /_static/ex1.png
  :width: 400
  :alt: Example 1 image

Defined Colours
=================
Specifying a colour map and the default square colour
::

    import pandas as pd
    from cccalendar import draw_colour_calendar
    my_data = pd.Series({
        '2021-01-01': 'event_one',
        '2021-01-07': 'event_two',
        '2021-01-10': 'event_three',
        '2021-01-14': 'event_four',
        '2021-01-19': 'event_one',
        '2021-01-23': 'event_two',
    })
    colour_map = {
        'event_one': 'b',
        'event_two': 'xkcd:green',
        'event_three': (255/255, 0/255, 255/255), # rgb
        'event_four': 'c'
    }
    draw_colour_calendar(my_data, colour_map, date_colour='#f64b00')

.. image:: /_static/ex2.png
  :width: 400
  :alt: Example 2 image