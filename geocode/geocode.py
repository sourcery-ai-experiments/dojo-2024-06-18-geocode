#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
import csv
from pathlib import Path

import pandas as pd
from geopy import ArcGIS
from tqdm import tqdm

assert tqdm
data_dir = Path(__file__).parent / "data"


def _get_known_locations(geocoded_csv: Path) -> set[str]:
    known_locations = set()
    with open(geocoded_csv) as fin:
        sheet = csv.DictReader(fin)
        for row in sheet:
            known_locations.add((row["address"]))
    return known_locations


def geocode():
    """Adds lat, lon columns to df."""

    geocoded_csv = data_dir / "geocoded.csv"
    known_locations = _get_known_locations(geocoded_csv)

    with open(geocoded_csv, "w") as fout:
        fields = "address,city,st,zip,housenum,street,lat,lon"
        sheet = csv.DictWriter(fout, fieldnames=fields.split(","))
        if len(known_locations) == 0:
            sheet.writeheader()

        geolocator = ArcGIS()
        for _, row in pd.read_csv(data_dir / "resident_addr.csv").iterrows():
            if row.address in known_locations:
                continue
            addr = f"{row.address}, {row.city}, {row.st} {row.zip}"
            location = geolocator.geocode(addr)
            if location:
                row = dict(row)
                row["lat"] = round(location.latitude, 5)
                row["lon"] = round(location.longitude, 5)
                sheet.writerow(row)
                fout.flush()
                print(end=".", flush=True)
                yield dict(row)
            else:
                print(f"Could not geocode {addr}")


def main() -> None:
    df = pd.DataFrame(geocode())
    print(df)
    df.to_csv(data_dir / "geocoded.csv", index=False)


if __name__ == "__main__":
    main()
