# Dataset provenance

## Primary dataset: UCI Online Retail

- Source: [UCI Machine Learning Repository — Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)
- DOI: https://doi.org/10.24432/C5BW33
- Author attribution: Chen, D. (2015). Online Retail. UCI Machine Learning Repository.
- License stated by UCI: Creative Commons Attribution 4.0 International (CC BY 4.0).
- Coverage: 1 December 2010 – 9 December 2011.
- Published source size: 541,909 transaction rows.

The original workbook is not committed to this repository. Download it with:

```bash
python scripts/download_data.py
```

The workbook will be saved under data/raw/ and is excluded from Git. The downloader retrieves the file from the official UCI repository.

## Included preview data

sample_transactions.csv is a small, hand-authored synthetic fixture for offline tests and the dashboard preview. It is not a subset of the UCI records and must not be used as evidence of real business performance.

## Attribution

When reusing this project or its processed outputs, credit the original UCI dataset and its DOI. Preserve the CC BY 4.0 attribution requirements described on the source page.
