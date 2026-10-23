# Homework 5: data cleaning

This is a runnable portfolio edition of the Python workflow in my original
homework notebook. It renames the misspelled `No_Pation` column, imputes missing
`HbA1c` values using the column mean, drops rows with other missing values,
normalizes the `CLASS` labels, removes `Cr` values above the 99.5th percentile,
and removes duplicate rows. The script reports how many rows each stage changes.

```bash
python -m pip install -r requirements.txt
python homework/05-data-cleaning/clean_diabetes.py input.csv cleaned.csv
python -m pytest -q
```

Run these commands from the repository root. `input.csv` must contain `Cr`,
`HbA1c`, and `CLASS`; the original homework input also has `No_Pation`.
The output path must differ from the input path. Set `--cr-quantile 0.99` to
try another cutoff. The original patient-level CSV and notebook outputs are
excluded from this public repository. The notebook used a strict `<` at the
cutoff, which also removed rows tied with it; this edition retains those ties
with `<=` and writes a CSV without an extra index column. Its row count can
therefore differ from the 2024 submitted file.

The [submitted report](../05-data-cleaning.pdf) documents the original work.
