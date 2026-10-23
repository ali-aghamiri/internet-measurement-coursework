"""Reproducible version of the cleaning workflow from homework five.

The original notebook is a 2024 course submission. This script preserves its
main steps while making the input, output, and row-removal rules explicit.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def clean_frame(frame: pd.DataFrame, cr_quantile: float = 0.995) -> tuple[pd.DataFrame, dict[str, int]]:
    """Clean one table, returning the cleaned table and processing counts."""
    if not 0 < cr_quantile < 1:
        raise ValueError("cr_quantile must be between 0 and 1 (exclusive)")

    required = {"Cr", "HbA1c", "CLASS"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"missing required columns: {', '.join(sorted(missing))}")
    if "No_Pation" in frame and "Patients_No" in frame:
        raise ValueError("input contains both No_Pation and Patients_No")

    cleaned = frame.rename(columns={"No_Pation": "Patients_No"}).copy()
    cleaned["Cr"] = pd.to_numeric(cleaned["Cr"], errors="coerce")
    cleaned["HbA1c"] = pd.to_numeric(cleaned["HbA1c"], errors="coerce")
    mean_hba1c = cleaned["HbA1c"].mean()
    if pd.isna(mean_hba1c):
        raise ValueError("HbA1c has no valid values for mean imputation")

    counts = {"input_rows": len(cleaned), "imputed_hba1c": int(cleaned["HbA1c"].isna().sum())}
    cleaned["HbA1c"] = cleaned["HbA1c"].fillna(mean_hba1c)
    before = len(cleaned)
    cleaned = cleaned.dropna().copy()
    counts["dropped_missing"] = before - len(cleaned)
    if cleaned.empty:
        raise ValueError("no rows remain after removing missing values")

    cleaned["CLASS"] = cleaned["CLASS"].astype(str).str.strip().str.upper()
    threshold = cleaned["Cr"].quantile(cr_quantile)
    before = len(cleaned)
    cleaned = cleaned.loc[cleaned["Cr"] <= threshold].copy()
    counts["dropped_high_cr"] = before - len(cleaned)
    before = len(cleaned)
    cleaned = cleaned.drop_duplicates().reset_index(drop=True)
    counts["dropped_duplicates"] = before - len(cleaned)
    counts["output_rows"] = len(cleaned)
    return cleaned, counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="input CSV with the original homework schema")
    parser.add_argument("output", type=Path, help="new path for the cleaned CSV")
    parser.add_argument(
        "--cr-quantile", type=float, default=0.995,
        help="upper Cr quantile; rows above it are removed (default: 0.995)",
    )
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error("input and output must be different files")
    try:
        cleaned, counts = clean_frame(pd.read_csv(args.input), args.cr_quantile)
    except (OSError, ValueError, pd.errors.ParserError) as error:
        parser.error(str(error))
    cleaned.to_csv(args.output, index=False)
    print(f"Saved {counts['output_rows']} rows to {args.output}")
    print(", ".join(f"{name}={value}" for name, value in counts.items()))


if __name__ == "__main__":
    main()
