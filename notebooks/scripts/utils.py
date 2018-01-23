# Standard Python built-in libraries
from functools import partial
from bokeh.plotting import figure
from datashader.utils import lnglat_to_meters as webm
from datashader.utils import export_image
from datashader.colors import colormap_select


# Set default plot width (we compute the plot height)
PLOT_WIDTH = 750
BACKGROUND = "black"


def add_webm_xys(df):
  """computer Mercator x and y values from Longitude and Latitude"""

  x, y = [c for c in list(webm(df.loc[:, 'Longitude'], df.loc[:, 'Latitude']))]
  df = df.assign(webm_x=x).copy()
  df = df.assign(webm_y=y).copy()
  return df


def get_plot_size(x_range, y_range, plot_width=PLOT_WIDTH):
  """returns a tuple (plot_width, plot_height) in pixels

    Args:
      x_range (float): bounding box Web Mercator tuple X range in meters (min_x, max_x)
      y_range (float): bounding box Web Mercator tuple Y range in meters (min_y, max_y)
      plot_width (int): the desirable plot width in pixel

    Returns:
      plot_width (int), plot_height (int)

  """

  # compute X and Y distances
  x_range_dist = x_range[1] - x_range[0]
  y_range_dist = y_range[1] - y_range[0]
  plot_height = int(y_range_dist * plot_width /x_range_dist)
  return (plot_width, plot_height)


def get_plot_params(bbox, plot_width=PLOT_WIDTH):
  """returns the Web Mercator x_range and y_range in meters, and plot_width and plot_height in pixels.

  Args:
    bbox: bounding box Web Mercator tuple (longitude_range, latitude_range) in degrees.
          i.e. ((min_longitude, max_latitude), (min_latitude, max_latitude))
    plot_width (int): the desirable plot width in pixel

  Returns:
    x_range, y_range, plot_width, plot_height

  """
  x_range, y_range = webm(*bbox)
  plot_width, plot_height = get_plot_size(x_range, y_range, plot_width=plot_width)
  return x_range, y_range, plot_width, plot_height


def base_plot(x_range, y_range, plot_width, plot_height, tools='pan, wheel_zoom, reset, save', **plot_args):
  """returns a Bokeh figure object with default parameters"""

  p = figure(
    x_range=x_range, y_range=y_range, plot_width=plot_width, plot_height=plot_height,
    tools=tools, outline_line_color=None, min_border=0,
    min_border_left=0, min_border_right=0, min_border_top=0, min_border_bottom=0,
    **plot_args)

  p.axis.visible = False
  p.xgrid.grid_line_color = None
  p.ygrid.grid_line_color = None
  return p


# utility function: to enable us to export a plot to an image file, with default parameters (e.g. background)
export = partial(export_image, background=BACKGROUND, export_path="export")

# utility function: color map
cm = partial(colormap_select, reverse=(BACKGROUND!="black"))