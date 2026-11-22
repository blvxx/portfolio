from __future__ import annotations

import argparse
import shutil
import urllib.request
import zipfile
from pathlib import Path

DATA_URL = "https://archive.ics.uci.edu/static/public/352/online+retail.zip"
DEFAULT_DESTINATION = Path(__file__).resolve().parents[1] / "data" / "raw" / "Online Retail.xlsx"


def download(destination: Path = DEFAULT_DESTINATION, force: bool = False) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not force:
        print("Dataset already exists:", destination)
        return destination

    archive = destination.with_suffix(".zip")
    print("Downloading the UCI Online Retail dataset...")
    request = urllib.request.Request(
        DATA_URL,
        headers={"User-Agent": "customer-retention-analytics/1.0"},
    )
    with urllib.request.urlopen(request, timeout=90) as response, archive.open("wb") as output:
        shutil.copyfileobj(response, output)

    try:
        with zipfile.ZipFile(archive) as zipped:
            workbook = next(
                (name for name in zipped.namelist() if Path(name).name.lower() == "online retail.xlsx"),
                None,
            )
            if workbook is None:
                raise FileNotFoundError("Online Retail.xlsx was not found inside the UCI archive.")
            with zipped.open(workbook) as source, destination.open("wb") as output:
                shutil.copyfileobj(source, output)
    finally:
        archive.unlink(missing_ok=True)

    print("Saved dataset:", destination)
    return destination


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download the UCI Online Retail workbook.")
    parser.add_argument("--force", action="store_true", help="Download again even if the workbook exists.")
    args = parser.parse_args()
    download(force=args.force)
