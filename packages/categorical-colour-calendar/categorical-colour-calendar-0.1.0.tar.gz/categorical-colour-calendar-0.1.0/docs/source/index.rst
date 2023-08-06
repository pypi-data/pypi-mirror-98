Welcome to Categorical Colour Calendar's documentation!
=======================================================

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   pages/getting_started
   pages/functionality
   pages/reference
   pages/examples

Categorical Colour Calendar allows you to plot monthly calendars and highlight discrete data.

It was created as existing solutions for plotting calendars were tailored toward continuous data and thus produced heatmaps (e.g. calmap, calplot).

These other solutions also generated yearly calendar figures (in the style of GitHub contributions chart), rather than a more familiar monthly calendar.

It is reasonably customizable, with a range of parameters controlling the behaviour the resultant plot.

The library can be used in a few different ways:

* The most simple is to provide a Series of events with a date index and the rest will be taken care of, including event-colour mapping generation.

* You can also provide a dictionary mapping your events to the desired colour.

* The most verbose usage is to provide a Series with daily values and corresponding colour map, giving full control over the colour of each date.

There are further parameters controlling other aspects of the figure.

Categorical Colour Calendar uses Matplotlib to render shapes on an axis and handle colour values.

.. image:: /_static/colourful.png
  :width: 800
  :alt: Sample calendar figure

*A colourful example*
