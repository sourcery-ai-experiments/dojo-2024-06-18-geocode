#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
"""
Display a map of residences in southern San Mateo County.
"""
from collections.abc import Generator

import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.basemap import Basemap

from geocoding.display_bay_area import get_residences

light_brown = "#E7B36A"


def display_filtered_san_mateo_map() -> None:
    scale_loc = -122.1425, 37.452
    m = Basemap(
        projection="merc",
        urcrnrlat=37.48,
        llcrnrlat=37.45,
        lat_ts=37,
        llcrnrlon=-122.155,
        urcrnrlon=-122.12,
        resolution="i",
    )
    m.fillcontinents(color=light_brown, lake_color="aqua")
    m.drawcounties()
    m.drawmapscale(*scale_loc, *scale_loc, 2, barstyle="fancy")
    plt.title("San Mateo")

    df = pd.DataFrame(_get_rows(m))
    for _, row in df.iterrows():
        m.plot(row.x, row.y, "bo", markersize=5)
    plt.show()


def _get_rows(m: Basemap) -> Generator[dict[str, float | str], None, None]:
    for lon, lat, addr in get_residences():
        x, y = m(lon, lat)
        yield {"x": x, "y": y, "addr": addr}


if __name__ == "__main__":
    display_filtered_san_mateo_map()
