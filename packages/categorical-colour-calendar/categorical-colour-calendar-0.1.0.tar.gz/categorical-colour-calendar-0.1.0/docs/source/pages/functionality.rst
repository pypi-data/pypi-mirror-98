##############################################
Functionality
##############################################

The ``draw_colour_calendar`` method will produce a calendar for every month between the month of the earliest date and the
latest date in the data provided. For example if you provided a Series which spanned from 31/01 to 01/03, it will
draw January, February and March in their entirety.

Supported colours include all the Matplotlib `named colours <https://matplotlib.org/stable/gallery/color/named_colors.html>`_
as well as RGB and RGBA values, expressed in the form (r=R/255, g=G/255, b=B/255) such that *0 <= r,g,b <= 1*.
This set of colours corresponds to those supported by the matplotlib.colors.to_hex() method.
This means HSV values are not supported.

When colours for one or more events are not provided (and ``generate_colours`` isn't set to ``False``), new colours
will be generated. These will have evenly spaced hue values with pre-determined saturation and lightness values. However there
is no guarantee the newly generated colours will not be similar to any colours provided by the user.

There is one other public method, ``draw_month_calendar``, detailed in :ref:`reference<Reference>`
but not mentioned elsewhere. This can be used to draw a calendar for a specific month.
It does not include any of the helper functionality when calling ``draw_colour_calendar`` directly so you must provide a
Series with a valid colour value for every date in the month.

If there are multiple events present for the same date (i.e a duplicated index), the date square will have a split colour.