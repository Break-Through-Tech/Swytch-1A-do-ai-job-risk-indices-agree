"""Task 8: simple per-index EDA and percentile ranks.

Run from the repository root: python notebooks/task8_eda_ranks.py
Requires openpyxl, which is already listed in requirements.txt.
"""

import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/datasets"
OUT = DATA / "processed"
FIGURES = ROOT / "figures"
SCORES = {
    "aioe": "AIOE",
    "fo_prob": "Frey–Osborne probability",
    "dv_rating_beta": "Eloundou GPT-4 beta",
    "human_rating_beta": "Eloundou human beta",
}


def read_csv(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def number(value):
    return float(value) if value not in (None, "") else None


def percentile_ranks(values):
    """Average tied positions divided by the number of nonmissing values."""
    indexed = sorted((value, i) for i, value in enumerate(values) if value is not None)
    result = [None] * len(values)
    start = 0
    while start < len(indexed):
        end = start + 1
        while end < len(indexed) and indexed[end][0] == indexed[start][0]:
            end += 1
        rank = ((start + 1) + end) / 2 / len(indexed)
        for _, original_index in indexed[start:end]:
            result[original_index] = rank
        start = end
    return result


def quantile(sorted_values, fraction):
    position = (len(sorted_values) - 1) * fraction
    low = math.floor(position)
    high = math.ceil(position)
    return sorted_values[low] + (sorted_values[high] - sorted_values[low]) * (position - low)


def spearman(pairs):
    # Re-rank on the pairwise complete sample, including average ranks for ties.
    x = percentile_ranks([a for a, _ in pairs])
    y = percentile_ranks([b for _, b in pairs])
    mx, my = statistics.mean(x), statistics.mean(y)
    numerator = sum((a - mx) * (b - my) for a, b in zip(x, y))
    denominator = math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))
    return numerator / denominator


def histogram_svg(values, label, path, bins=20):
    low, high = min(values), max(values)
    counts = [0] * bins
    for value in values:
        index = min(bins - 1, int((value - low) / (high - low) * bins))
        counts[index] += 1
    width, height = 720, 300
    plot_left, plot_top, plot_width, plot_height = 65, 45, 620, 195
    bars = []
    for index, count in enumerate(counts):
        bar_height = count / max(counts) * plot_height
        x = plot_left + index * plot_width / bins
        y = plot_top + plot_height - bar_height
        bars.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{plot_width / bins - 2:.1f}" height="{bar_height:.1f}" fill="#3978a8"/>')
    from xml.sax.saxutils import escape

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="white"/>
<text x="{plot_left}" y="25" font-family="sans-serif" font-size="17">{escape(label)} (n={len(values)})</text>
<line x1="{plot_left}" y1="{plot_top + plot_height}" x2="{plot_left + plot_width}" y2="{plot_top + plot_height}" stroke="#333"/>
<line x1="{plot_left}" y1="{plot_top}" x2="{plot_left}" y2="{plot_top + plot_height}" stroke="#333"/>
{''.join(bars)}
<text x="{plot_left}" y="265" font-family="sans-serif" font-size="12">{low:.3f}</text>
<text x="{plot_left + plot_width}" y="265" text-anchor="end" font-family="sans-serif" font-size="12">{high:.3f}</text>
<text x="{plot_left}" y="285" font-family="sans-serif" font-size="12">20 equal-width bins; y-axis = occupations</text>
</svg>'''
    path.write_text(svg, encoding="utf-8")


def source_check(rows, score, source_path, code_column, value_column):
    source = defaultdict(list)
    for row in read_csv(source_path):
        value = number(row[value_column])
        if row[code_column] and value is not None:
            source[row[code_column]].append(value)
    checked = []
    for row in rows:
        values = source[row["soc2018"]]
        observed = number(row[score])
        if not values or observed is None:
            continue
        expected = statistics.mean(values)
        checked.append((row["soc2018"], math.isclose(observed, expected, abs_tol=1e-10)))
    return checked


def main():
    rows = read_csv(OUT / "merged_v0.csv")
    assert len(rows) == len({row["soc2018"] for row in rows}) == 798
    FIGURES.mkdir(exist_ok=True)
    report = ["# Task 8 — Per-index EDA and percentile ranks", "",
              "Input: `data/datasets/processed/merged_v0.csv` (798 distinct 2018 SOC occupations).",
              "Higher scores and ranks mean more exposed or automatable within each measure.",
              "Missing scores remain blank. Ties receive their average rank; percentile = rank / nonmissing count.",
              "These measures have different meanings, so raw score magnitudes are not compared across indices.", "",
              "## Summary", "", "| Score | N | Missing | Min | P25 | Median | P75 | Max | Mean |",
              "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for score, label in SCORES.items():
        values = [number(row[score]) for row in rows]
        ranked = percentile_ranks(values)
        for row, rank in zip(rows, ranked):
            row["rank_" + score] = "" if rank is None else f"{rank:.12g}"
        observed = sorted(value for value in values if value is not None)
        report.append(f"| {label} | {len(observed)} | {len(rows)-len(observed)} | {observed[0]:.3f} | {quantile(observed,.25):.3f} | {quantile(observed,.5):.3f} | {quantile(observed,.75):.3f} | {observed[-1]:.3f} | {statistics.mean(observed):.3f} |")
        histogram_svg(observed, label, FIGURES / f"task8_{score}.svg")
    zones = {zone: sum(row["job_zone"] == zone for row in rows) for zone in ("1", "2", "3", "4", "5")}
    assert sum(zones.values()) == len(rows), "Unexpected missing or invalid Job Zone"
    report += ["", "## O*NET Job Zone", "",
               "Job Zone is an ordinal preparation measure, so its distribution is shown as counts rather than an exposure percentile rank.", "",
               "| Zone | Jobs |", "| ---: | ---: |"]
    report += [f"| {zone} | {count} |" for zone, count in zones.items()]
    report.append("")
    report += ["", "## Extreme occupations", "",
               "The five lowest and highest available values per index are listed below. Ties are ordered by SOC code.", ""]
    for score, label in SCORES.items():
        available = [row for row in rows if row[score] != ""]
        ordered = sorted(available, key=lambda row: (float(row[score]), row["soc2018"]))
        report += [f"### {label}", "", "| End | SOC | Occupation | Score |", "| --- | --- | --- | ---: |"]
        highest = sorted(available, key=lambda row: (-float(row[score]), row["soc2018"]))[:5]
        for end, selected in (("Low", ordered[:5]), ("High", highest)):
            for row in selected:
                report.append(f"| {end} | {row['soc2018']} | {row['title'].replace('|','/')} | {float(row[score]):.3f} |")
        report.append("")
    pairs = [(number(row["aioe"]), number(row["fo_prob"])) for row in rows]
    pairs = [(a,b) for a,b in pairs if a is not None and b is not None]
    report += ["## Initial cross-index check", "",
               f"AIOE vs Frey–Osborne: Spearman rho = **{spearman(pairs):.3f}**, using **{len(pairs)}** jobs with both scores. This is descriptive agreement between rankings, not agreement about job loss.", ""]
    checks = {
        "aioe": source_check(rows, "aioe", OUT / "aioe_2018soc.csv", "soc2018", "aioe"),
        "fo_prob": source_check(rows, "fo_prob", OUT / "frey_osborne_2018soc.csv", "soc2018", "fo_prob"),
        "dv_rating_beta": source_check(rows, "dv_rating_beta", DATA / "eloundou_6digit.csv", "soc_6digit", "dv_rating_beta"),
        "human_rating_beta": source_check(rows, "human_rating_beta", DATA / "eloundou_6digit.csv", "soc_6digit", "human_rating_beta"),
    }
    report += ["## Score trace checks", "",
               "Recomputed each available merged score from its prepared input. AIOE and Frey–Osborne repeat mapped source rows are averaged, matching Task 6. These checks verify the join and rollup; the source papers' estimates are not independently validated.", ""]
    for score_column, checked in checks.items():
        failures = [code for code, okay in checked if not okay]
        expected_count = sum(number(row[score_column]) is not None for row in rows)
        assert len(checked) == expected_count, f"{score_column}: not every merged score was traced"
        report.append(f"- {SCORES[score_column]}: {len(checked)} values checked; {len(failures)} mismatches" + (f" ({', '.join(failures[:10])})" if failures else "") + ".")
        assert not failures, f"{score_column} source check failed: {failures[:10]}"
    # Spot-check selected extremes against the original files, not only prepared tables.
    from openpyxl import load_workbook

    workbook = load_workbook(DATA / "AIOE_appendixA.xlsx", read_only=True, data_only=True)
    aioe_raw = {str(code): float(value) for code, _, value in list(workbook["Appendix A"].values)[1:] if code and value is not None}
    fo_raw = {row["soc_code_2010"]: float(row["fo_computerization_probability"])
              for row in read_csv(DATA / "frey_osborne_probabilities.csv")}
    elo_raw = {row["O*NET-SOC Code"]: row for row in read_csv(DATA / "occ_level.csv")}
    by_code = {row["soc2018"]: row for row in rows}
    spots = [
        ("aioe", "27-2031", aioe_raw, "aioe_source_codes"),
        ("aioe", "29-9092", aioe_raw, "aioe_source_codes"),
        ("fo_prob", "29-1125", fo_raw, "fo_source_codes"),
        ("fo_prob", "51-9151", fo_raw, "fo_source_codes"),
        ("dv_rating_beta", "27-2021", elo_raw, None),
        ("dv_rating_beta", "15-2021", elo_raw, None),
        ("human_rating_beta", "13-1074", elo_raw, None),
        ("human_rating_beta", "19-3022", elo_raw, None),
    ]
    report += ["", "## Original-file spot checks of extremes", "",
               "For these occupations, the merged score matches the original AIOE workbook, Frey–Osborne CSV, or Eloundou occupation CSV. Each selected occupation has one original source row.", "",
               "| Score | SOC | Original value | Merged value |", "| --- | --- | ---: | ---: |"]
    for score, code, raw, source_codes_column in spots:
        row = by_code[code]
        if source_codes_column:
            source_codes = row[source_codes_column].split(";")
            assert len(source_codes) == 1
            original = raw[source_codes[0]]
        else:
            original = float(raw[code + ".00"][score])
        merged = float(row[score])
        assert math.isclose(original, merged, abs_tol=1e-10), (score, code, original, merged)
        report.append(f"| {SCORES[score]} | {code} | {original:.6f} | {merged:.6f} |")
    report += [
        "", "## What this first pass shows", "",
        "- The eight checked extremes match their original files, so these examples are not transcription or join errors. This does not validate the research estimates themselves.",
        "- Frey–Osborne is missing for 135 of the 798 merged jobs. The correlation uses the 663 jobs with both scores and should not be generalized to the missing jobs.",
        "- AIOE and Frey–Osborne rank these shared jobs differently: their Spearman correlation is negative. This is plausible because AIOE measures AI exposure while Frey–Osborne estimates computerisation probability; it is not evidence that either source is wrong.",
        "- The highest occupations differ by measure: Genetic Counselors lead AIOE, Photographic Process Workers are among the Frey–Osborne maximum ties, Mathematicians lead GPT-4 beta, and Survey Researchers tie at the top of human beta. The full extreme lists above make those differences reviewable.",
        "- Job Zone is the available O*NET summary measure used here. The many individual O*NET ability, skill, activity, and context features are reserved for the later grouped-feature modeling task.",
    ]
    report += ["", "## Reproduce", "", "Run `python notebooks/task8_eda_ranks.py` from the repository root. Outputs are `task8_ranked.csv`, this report, and four SVG histograms in `figures/`.", ""]
    with (OUT / "task8_ranked.csv").open("w", newline="", encoding="utf-8") as handle:
        columns = ["soc2018", "title", *SCORES, *("rank_" + score for score in SCORES)]
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (ROOT / "task8_report.md").write_text("\n".join(report), encoding="utf-8")
    print(f"Wrote rankings for {len(rows)} occupations and task8_report.md")


if __name__ == "__main__":
    main()
