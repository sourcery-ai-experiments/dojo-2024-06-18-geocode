#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
"""
Display a web page map of residences in southern San Mateo County.
"""
import matplotlib.pyplot as plt
import pandas as pd
from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter
from flask import Flask
from mpl_toolkits.basemap import Basemap

from geocoding.display_3_san_mateo import (
    _get_rows,
    light_brown,
    san_mateo_png,
    scale_loc,
)

app = Flask(__name__)


@app.route("/cached_map")  # type: ignore [misc]
def cached_san_mateo_map() -> tuple[bytes, int, dict[str, str]]:
    return san_mateo_png.read_bytes(), 200, {"Content-Type": "image/png"}


@app.route("/")  # type: ignore [misc]
def index() -> str:
    return prettify(
        title("map of San Mateo") + "<div style='font-size: 2em; margin: 3em;'>"
        "<hr><p>hello world</p><hr>"
        "<ul><li><a href='/cached_map'>San Mateo Map</a>"
    )


def title(text: str) -> str:
    return f"<!DOCTYPE html><html lang='en'><head><title>{text}</head><body>"


def prettify(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    return soup.prettify(formatter=HTMLFormatter(indent=2)).replace("<hr/>", "<hr>")


def display_filtered_san_mateo_map() -> None:
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
    print(df)
    for _, row in df.iterrows():
        m.plot(row.x, row.y, "bo", markersize=3)

    plt.savefig(san_mateo_png)
    plt.show()


if __name__ == "__main__":
    app.run(debug=True)
