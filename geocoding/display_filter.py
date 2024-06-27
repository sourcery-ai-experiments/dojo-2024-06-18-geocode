#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
"""
Display a map of residences in southern San Mateo County.
"""
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

from geocoding.display_bay_area import get_residences

dojo = (-122.049020, 37.3963152)  # 855 W Maude Ave, Mtn. View


def display_filtered_san_mateo_map() -> None:
    m = Basemap(
        projection="merc",
        urcrnrlat=37.48,
        llcrnrlat=37.45,
        lat_ts=37,
        llcrnrlon=-122.155,
        urcrnrlon=-122.12,
        resolution="h",
    )
    plt.title("San Mateo")

    for lon, lat, addr in get_residences():
        x, y = m(lon, lat)
        m.plot(x, y, "bo", markersize=5)
    plt.show()


if __name__ == "__main__":
    display_filtered_san_mateo_map()
