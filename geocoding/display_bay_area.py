#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
"""
Display a map of the San Francisco Bay Area,
with a scale indication plotted at the location of the Hacker Dojo.

This comes straight from the Basemap tutorial.
"""
import matplotlib.pyplot as plt
import numpy as np
from geocode import data_dir
from mpl_toolkits.basemap import Basemap

dojo = (-122.049020, 37.3963152)  # 855 W Maude Ave, Mtn. View


def display_bay_area_map() -> None:
    assert data_dir.exists()
    m = Basemap(
        projection="merc",
        urcrnrlat=38,
        llcrnrlat=37.2,
        lat_ts=37,
        llcrnrlon=-122.6,
        urcrnrlon=-121.8,
        resolution="h",
    )
    m.drawcoastlines()
    m.fillcontinents(color="coral", lake_color="aqua")
    m.drawcounties()
    m.drawmapscale(*dojo, *dojo, 10, barstyle="fancy")

    m.drawparallels(np.arange(30.0, 50.0, 0.1))
    m.drawmeridians(np.arange(-130.0, -110.0, 0.1))
    m.drawmapboundary(fill_color="aqua")
    plt.title("Mercator Projection")
    plt.show()


if __name__ == "__main__":
    display_bay_area_map()
