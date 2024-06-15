#! /usr/bin/env _TYPER_STANDARD_TRACEBACK=1 python
# Copyright 2024 John Hanley. MIT licensed.
import re
from collections.abc import Generator
from pathlib import Path

import pandas as pd
import seaborn as sns
import typer
from matplotlib import pyplot as plt


def _get_rows(input_logfile: Path) -> Generator[dict[str, float], None, None]:
    seconds_re = re.compile(r"^(\w+): *([\d\.]+) *seconds$")
    row = []
    for line in input_logfile.read_text().splitlines():
        m = seconds_re.search(line)
        if m:
            row.append((m[1].lower(), float(m[2])))
            if m[1] == "Multiprocessing":
                yield dict(sorted(row))
                row.clear()


def speed_chart(input_logfile: Path = Path("/tmp/timings.txt")) -> None:
    df = pd.DataFrame(_get_rows(input_logfile))
    print(df.describe())

    csv = input_logfile.with_suffix(".csv")
    df.to_csv(csv, index=False)

    sns.catplot(data=df)
    plt.show()


if __name__ == "__main__":
    typer.run(speed_chart)
