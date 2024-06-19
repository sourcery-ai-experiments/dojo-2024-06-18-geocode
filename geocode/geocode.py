#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.

from pathlib import Path

import pandas as pd
from geopy import ArcGIS
from tqdm import tqdm

assert tqdm
data_dir = Path(__file__).parent / "data"


def geocode(df: pd.DataFrame) -> pd.DataFrame:
    """Adds lat, lon columns to df."""
    geolocator = ArcGIS()
    rows = [row for _, row in df.iterrows()]
    for row in rows:
        addr = f"{row.address}, {row.city}, {row.st} {row.zip}"
        location = geolocator.geocode(addr)
        if location:
            row["lat"] = round(location.latitude, 5)
            row["lon"] = round(location.longitude, 5)
        else:
            print(f"Could not geocode {addr}")
        print("\n", row.lat, "\t", row.lon, "\t", addr)
    return df


def main() -> None:
    df = pd.read_csv(data_dir / "resident_addr.csv")

    df = geocode(df)
    df.to_csv(data_dir / "geocoded.csv", index=False)


if __name__ == "__main__":
    main()
