

from pathlib import Path

from energycharts import (
  daily_calendar_chart,
  generate_example_daily_usage_data,
  generate_example_profile_data,
  heatmap_chart,
  load_duration_chart,
)


def calendar_example():
  df= generate_example_daily_usage_data()
  days = df["date"].to_list()
  values = df["value"].to_list()
  fig = daily_calendar_chart(days, values, "Daily Usage Example")
  out_dir = Path('examples')
  out_dir.mkdir(exist_ok=True)
  out_fp = out_dir / "calendar_example.png"
  fig.savefig(out_fp, bbox_inches="tight")


def ldc_example():
  df= generate_example_profile_data(include_export=True)
  fig = load_duration_chart(
    df["ts"].to_list(),
    df["value"].to_list(),
    "Load Duration Curve Example",
  )
  fig.show()

def heatmap_example():
  df= generate_example_profile_data(include_export=True)
  fig = heatmap_chart(
    df["ts"].to_list(),
    df["value"].to_list(),
    "Heatmap Example",
  )
  fig.show()

#calendar_example()
#ldc_example()
heatmap_example()



