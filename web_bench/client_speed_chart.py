#! /usr/bin/env _TYPER_STANDARD_TRACEBACK=1 python
# Copyright 2024 John Hanley. MIT licensed.
import re
from collections.abc import Generator
from pathlib import Path

import pandas as pd
import seaborn as sns
import typer
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.backends.backend_pdf import PdfPages
from seaborn import FacetGrid


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

    def savefig(pdf: PdfPages, fig: Axes | FacetGrid) -> None:
        assert fig
        pdf.savefig()  # type: ignore [no-untyped-call]
        plt.close()

    with PdfPages(input_logfile.with_suffix(".pdf"), keep_empty=False) as pdf:  # type: ignore [no-untyped-call]
        savefig(pdf, sns.boxplot(data=df))
        savefig(pdf, sns.catplot(data=df))
        savefig(pdf, sns.violinplot(data=df))
        savefig(pdf, sns.kdeplot(data=df))


if __name__ == "__main__":
    typer.run(speed_chart)
