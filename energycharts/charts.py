import logging
from datetime import date, datetime

import calplot
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Suppress matplotlib font manager log messages
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)


def daily_calendar_chart(
  days: list[date], values: list[float], title: str,textformat: str = ""):
  """Build calendar plot for given values"""
  vmin= min(values)
  vmax= max(values)
  day_dt= [datetime(d.year, d.month, d.day) for d in days]
  data = pd.Series(values, index=day_dt)
  plot = calplot.calplot(
    data,
    suptitle=title,
    how=None,
    vmin=vmin,
    vmax=vmax,
    textformat=textformat,
    cmap="YlOrRd",
    daylabels="MTWTFSS",
    colorbar=True,
  )
  fig = plot[0]
  return fig


def load_duration_chart(
  timestamps: list[datetime], values: list[float], title: str
) -> go.Figure:
  """Build load duration curve chart for given values"""

  data = list(zip(timestamps, values, strict=True))
  df= pd.DataFrame(data, columns=("ts", "value"))
  fig = px.ecdf(
    df,
    y="value",
    ecdfmode="complementary",
  )
  fig.update_layout(
    xaxis={"title": title, "dtick": 0.05, "tickformat": ",.0%", "range": [0, 1]},
  )
  return fig

def heatmap_chart(
  timestamps: list[datetime], values: list[float], title: str, units: str = ""
) -> go.Figure:
  first_day= min(timestamps).date()
  last_day= max(timestamps).date()
  num_days= (last_day- first_day).days
  min_value= min(values)

  data = list(zip(timestamps, values, strict=True))
  df= pd.DataFrame(data, columns=("ts", "value"))
  df.set_index("ts", inplace=True)

  colorscale= "Geyser" if min_value< 0 else "YlOrRd"
  midpoint = 0.0 if min_value< 0 else None

  nbinsx= 96
  nbinsy= num_days
  width = 800
  height = 200 + int(num_days* 0.5)
  fig = px.density_heatmap(
    df,
    title=title,
    width=width,
    height=height,
    x=df.index.date,
    y=df.index.time,
    z=df["value"],
    nbinsx=nbinsx,
    nbinsy=nbinsy,
    histfunc="avg",
    color_continuous_scale=colorscale,
    color_continuous_midpoint=midpoint,
  )
  fig.update_layout(
    xaxis_title=None,
    yaxis_title=None,
    margin=dict(l=20, r=20, t=25, b=20),
  )
  fig.update_layout(coloraxis=dict(colorbar=dict(title=units)))
  fig.update_xaxes(dtick="M1", tickformat="%b\n%Y", ticklabelmode="period")
  fig.update_yaxes(dtick=12, tickformat="%H:%M")
  return fig


