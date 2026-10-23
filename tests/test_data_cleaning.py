"""Checks the cleaned workflow against a small, synthetic table."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pandas as pd
import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "homework" / "05-data-cleaning" / "clean_diabetes.py"
spec = importlib.util.spec_from_file_location("clean_diabetes", SCRIPT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_cleaning_counts_and_values() -> None:
    rows = pd.DataFrame(
        [
            {"No_Pation": 1, "Cr": 1, "HbA1c": 6, "CLASS": "Y"},
            {"No_Pation": 2, "Cr": 2, "HbA1c": None, "CLASS": "Y "},
            {"No_Pation": 3, "Cr": 3, "HbA1c": None, "CLASS": "N"},
            {"No_Pation": 4, "Cr": None, "HbA1c": 5, "CLASS": "N"},
            {"No_Pation": 5, "Cr": 900, "HbA1c": 5, "CLASS": "P"},
            {"No_Pation": 1, "Cr": 1, "HbA1c": 6, "CLASS": "Y "},
        ]
    )
    result, counts = module.clean_frame(rows)

    assert counts == {
        "input_rows": 6,
        "imputed_hba1c": 2,
        "dropped_missing": 1,
        "dropped_high_cr": 1,
        "dropped_duplicates": 1,
        "output_rows": 3,
    }
    assert "Patients_No" in result and "No_Pation" not in result
    assert result["CLASS"].tolist() == ["Y", "Y", "N"]
    assert result["HbA1c"].tolist() == [6, 5.5, 5.5]


def test_constant_cr_values_are_kept() -> None:
    rows = pd.DataFrame({"Cr": [2, 2], "HbA1c": [5, 6], "CLASS": ["N", "Y"]})
    result, counts = module.clean_frame(rows)
    assert len(result) == 2
    assert counts["dropped_high_cr"] == 0


def test_missing_required_column_is_reported() -> None:
    with pytest.raises(ValueError, match="CLASS"):
        module.clean_frame(pd.DataFrame({"Cr": [1], "HbA1c": [5]}))
