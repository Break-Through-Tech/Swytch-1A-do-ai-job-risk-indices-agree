"""Prepare O*NET 30.3 occupation features for the Task 5 master join.

Run from the repository root with:
    .venv-1/bin/python notebooks/task5_onet_prep.py

The script preserves the raw files, writes five six-digit-SOC CSVs to
data/datasets/processed/, and records the feature-to-source mapping.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = REPO_ROOT / "data" / "datasets"
OUTPUT_DIR = INPUT_DIR / "processed"

SOC_COLUMN = "O*NET-SOC Code"
TITLE_COLUMN = "Title"


def six_digit_soc(code: pd.Series) -> pd.Series:
    """Convert an eight-digit O*NET-SOC code such as 11-1011.03 to 11-1011."""
    return code.astype(str).str.split(".", n=1).str[0]


def slug(text: str) -> str:
    """Make stable, readable, CSV-safe feature column names."""
    cleaned = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return cleaned


def title_lookup(data: pd.DataFrame) -> pd.DataFrame:
    """Prefer an occupation's .00 title; otherwise keep its first detail title."""
    titles = data[["soc_6digit", SOC_COLUMN, TITLE_COLUMN]].drop_duplicates().copy()
    titles["has_base_title"] = titles[SOC_COLUMN].str.endswith(".00")
    titles = titles.sort_values(
        ["soc_6digit", "has_base_title", SOC_COLUMN],
        ascending=[True, False, True],
    )
    titles = titles.drop_duplicates("soc_6digit").rename(
        columns={TITLE_COLUMN: "title"}
    )
    titles["title_rollup_method"] = titles["has_base_title"].map(
        {True: "base_00", False: "first_detail"}
    )
    return titles[["soc_6digit", "title", "title_rollup_method"]]


def validate_output(
    data: pd.DataFrame, label: str, expected_rows: int | None = None
) -> None:
    """Fail early if an output cannot safely be joined on six-digit SOC."""
    assert data["soc_6digit"].is_unique, f"{label}: duplicate six-digit SOC codes"
    assert data["soc_6digit"].str.fullmatch(r"\d{2}-\d{4}").all(), (
        f"{label}: invalid six-digit SOC code"
    )
    if expected_rows is not None:
        assert len(data) == expected_rows, (
            f"{label}: expected {expected_rows} SOC codes, found {len(data)}"
        )


def prepare_feature_table(
    source_files: list[tuple[str, str]],
    output_name: str,
    feature_prefix: str,
    scale_id: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Filter a long O*NET source to one scale, roll up, and pivot it wide."""
    frames: list[pd.DataFrame] = []

    for filename, sheet_name in source_files:
        source = pd.read_excel(INPUT_DIR / filename, sheet_name=sheet_name)
        source["source_workbook"] = filename
        frames.append(source)

    data = pd.concat(frames, ignore_index=True)
    data["soc_6digit"] = six_digit_soc(data[SOC_COLUMN])
    data = data.loc[data["Scale ID"].eq(scale_id)].copy()

    if data.empty:
        raise ValueError(f"{output_name}: no rows found for Scale ID {scale_id!r}")

    titles = title_lookup(data)

    # Average detailed specialties into one six-digit SOC value per O*NET element.
    rolled = (
        data.groupby(
            ["soc_6digit", "Element ID", "Element Name", "source_workbook"],
            as_index=False,
        )["Data Value"]
        .mean()
    )

    rolled["feature_column"] = rolled.apply(
        lambda row: f"{feature_prefix}_{slug(row['Element Name'])}__{slug(row['Element ID'])}",
        axis=1,
    )

    if rolled.duplicated(["soc_6digit", "feature_column"]).any():
        raise ValueError(f"{output_name}: duplicate SOC/feature values after rollup")

    wide = (
        rolled.pivot(index="soc_6digit", columns="feature_column", values="Data Value")
        .reset_index()
        .sort_values("soc_6digit")
    )
    output = titles.merge(wide, on="soc_6digit", how="right")
    output = output[["soc_6digit", "title", "title_rollup_method"] + [
        column
        for column in output.columns
        if column not in {"soc_6digit", "title", "title_rollup_method"}
    ]]
    validate_output(output, output_name)

    dictionary = (
        rolled[["source_workbook", "Element ID", "Element Name", "feature_column"]]
        .drop_duplicates()
        .rename(
            columns={
                "Element ID": "element_id",
                "Element Name": "element_name",
                "feature_column": "column_name",
            }
        )
    )
    dictionary.insert(0, "dataset", output_name.removesuffix("_6digit"))
    dictionary["scale_id"] = scale_id
    dictionary["rollup_rule"] = "mean of detailed O*NET occupations within six-digit SOC"

    return output, dictionary


def prepare_job_zones() -> pd.DataFrame:
    """Roll Job Zones to six digits, preserving the decision made for each SOC."""
    data = pd.read_excel(INPUT_DIR / "onet_job_zones.xlsx", sheet_name="Job Zones")
    data["soc_6digit"] = six_digit_soc(data[SOC_COLUMN])

    title_data = title_lookup(data)
    rows: list[dict[str, object]] = []

    for soc, group in data.groupby("soc_6digit", sort=True):
        base = group.loc[group[SOC_COLUMN].str.endswith(".00")]
        unique_zones = sorted(group["Job Zone"].unique())
        had_conflict = len(unique_zones) > 1

        if not base.empty:
            zone = int(base.iloc[0]["Job Zone"])
            method = "base_00"
        else:
            counts = group["Job Zone"].value_counts()
            modes = sorted(counts[counts.eq(counts.max())].index.tolist())
            zone = int(modes[0])
            method = "detail_mode" if len(modes) == 1 else "detail_mode_tie_lower"

        rows.append(
            {
                "soc_6digit": soc,
                "job_zone": zone,
                "job_zone_rollup_method": method,
                "job_zone_had_conflict": had_conflict,
                "job_zone_source_value_count": len(unique_zones),
            }
        )

    output = title_data.merge(pd.DataFrame(rows), on="soc_6digit", how="inner")
    validate_output(output, "onet_job_zones_6digit", expected_rows=798)
    assert output["job_zone"].between(1, 5).all(), "Job Zone must be between 1 and 5"
    return output


def write_csv(data: pd.DataFrame, filename: str) -> None:
    path = OUTPUT_DIR / filename
    data.to_csv(path, index=False)
    print(f"Wrote {path.relative_to(REPO_ROOT)}: {data.shape[0]} rows, {data.shape[1]} columns")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    dictionaries: list[pd.DataFrame] = []

    job_zones = prepare_job_zones()
    write_csv(job_zones, "onet_job_zones_6digit.csv")
    print(
        "  Job Zone conflicts retained in audit flags:",
        int(job_zones["job_zone_had_conflict"].sum()),
    )

    specifications = [
        (
            [("onet_abilities.xlsx", "Abilities")],
            "onet_abilities_6digit",
            "ability",
            "IM",
        ),
        (
            [
                ("onet_essential_skills.xlsx", "Essential Skills"),
                ("onet_transferable_skills.xlsx", "Transferable Skills"),
            ],
            "onet_skills_6digit",
            "skill",
            "IM",
        ),
        (
            [("onet_work_activities.xlsx", "Work Activities")],
            "onet_work_activities_6digit",
            "work_activity",
            "IM",
        ),
        (
            [("onet_work_context.xlsx", "Work Context")],
            "onet_work_context_6digit",
            "work_context",
            "CX",
        ),
    ]

    for source_files, output_name, prefix, scale in specifications:
        output, dictionary = prepare_feature_table(
            source_files, output_name, prefix, scale
        )
        write_csv(output, f"{output_name}.csv")
        dictionaries.append(dictionary)

    feature_dictionary = pd.concat(dictionaries, ignore_index=True).sort_values(
        ["dataset", "column_name"]
    )
    write_csv(feature_dictionary, "onet_feature_dictionary.csv")


if __name__ == "__main__":
    main()
