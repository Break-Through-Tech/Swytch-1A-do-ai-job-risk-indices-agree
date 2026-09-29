# SOC 2010 → 2018 Crosswalk: Handling Decisions

This document records how `crosswalk_clean.csv` handles every non-trivial
transformation between the 2010 SOC and 2018 SOC. Source: `soc_2010_to_2018_crosswalk.xlsx`
and its companion explanatory note (BLS, November 2017), cross-referenced against
the 2018 SOC Manual and 2018 SOC Definitions (BLS).

## ⚠️ Before using this document: verify cluster membership is complete

The cluster analysis below was built from a `pandas` `groupby`/`networkx`
connected-components pass. Initial printouts were **truncated by pandas' default
display settings** and may not show every code in each cluster. Before finalizing
any handling rule, re-run with full output and re-check membership:

```python
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_seq_items', None)
print(summary_df.to_string())
```

One known gap: `15-1243`'s (Database Architects) exclude clause names `15-1242`
(Database Administrators) as a sibling split — confirm whether `15-1242` belongs
in the mega-cluster below before treating that section as complete.

## Marker legend (confirmed from BLS explanatory note)

- `(#)` on a 2010 code = that occupation was **divided** into multiple 2018 codes (a split)
- `(##)` on a 2018 code = that occupation was **created by merging** multiple 2010 codes (a merge)
- Markers describe the transformation of the *specific marked code*, not the
  overall shape of a connected cluster — a cluster can be simultaneously a split
  on one side and a merge on the other (see mega-cluster below)

## Validation check

Total occupations gained across all clusters: **39**
Total occupations lost: **12**
Net change: **+27**

This matches the published headline difference between SOC revisions
(2010 SOC: 840 detailed occupations → 2018 SOC: 867), which is strong
independent confirmation the cluster analysis captured the full picture.

## Classification methodology

1. Built a graph with 2010 codes and 2018 codes as nodes, one edge per
   crosswalk row.
2. Found connected components. Components of size 2 (one 2010 code, one
   2018 code) are clean 1:1 matches — no special handling.
3. Larger components were classified by old/new code counts:
   - 1 old → N new = **split**
   - N old → 1 new = **merge**
   - N old → M new = **tangled** (investigated individually below)
4. Cross-referenced the 2018 SOC Definitions PDF (Excludes clauses) and the
   2018 SOC Manual's Table 3 ("occupations new to the 2018 SOC due to
   breakouts of 2010 SOC 'All Other' occupations') to disambiguate each
   tangled cluster.

## General handling rules

| Match type | Rule |
|---|---|
| 1:1 | Direct join, no transformation |
| 1:many (split) | Duplicate the source value across all resulting 2018 codes |
| many:1 (merge) | Mean of contributing source values (unweighted — no employment-weight source available) |
| tangled, resolved to a single hub + clean splits | Treat the hub as a many:1 merge (mean); treat all other codes in the cluster as ordinary 1:many splits from their own single parent |
| tangled, genuinely unresolved | Equal-weight duplicate/mean, explicitly flagged as a documented limitation |

## Per-cluster resolutions

### 1. Mega-cluster: Management/Business/Computer catch-alls → Project Management Specialists, etc.

**Old codes (confirmed, full list):** `11-9199`, `13-1199`, `15-1132`, `15-1133`, `15-1134`, `15-1141`, `15-1199`, `43-9011`
**New codes (confirmed, full list):** `11-9072`, `11-9179`, `11-9199`, `13-1082`, `13-1199`, `15-1242`, `15-1243`, `15-1252`, `15-1253`, `15-1254`, `15-1255`, `15-1299`

This is not one tangled reorganization — it's several clean splits that share
a hub node (`13-1082`), plus one small absorbed code.

- `11-9199` (old) → `11-9072` (carve-out: Entertainment/Recreation Managers) + `11-9179` (carve-out: Personal Service Managers, All Other) + `11-9199` (narrower continuation) + slice into `13-1082`
- `13-1199` (old) → `13-1199` (narrower continuation) + slice into `13-1082` (per BLS FAQ, this is the *dominant* contributor to `13-1082`)
- `15-1132`/`15-1133` (old Software Developers, Applications/Systems) → `15-1252` (Software Developers, general dev work) + `15-1253` (Software QA Analysts and Testers, testing-focused work)
- `15-1134` (old Web Developers) → `15-1254` (Web Developers, continuation) + `15-1255` (Web and Digital Interface Designers, new design-focused carve-out) — confirmed by full membership; `15-1254` is the "just renamed" sibling I flagged as missing last pass
- `15-1141` (old Database Administrators) → `15-1242` (Database Administrators, continuation) + `15-1243` (Database Architects, carve-out) — confirmed; `15-1242` was indeed the missing sibling
- `15-1199` (old Computer Occupations, All Other) → `15-1299` (rename, now narrower with 8 explicit exclusions) + slice into `13-1082`
- `43-9011` (old, 2010 office/administrative code "Computer Operators") → most likely `15-1299`. Current O*NET/BLS practitioner guidance explicitly redirects retired lookups for `43-9011` to `15-1299`. **Caveat:** the definition text for `15-1299` (and its 2010 predecessor `15-1199`) explicitly lists `43-9011` as *excluded* — a mild contradiction between the definitional exclude clause and the practical crosswalk destination. **Action:** verify directly by filtering the raw crosswalk for the `43-9011` row to see its literal target code, rather than relying on this inference:
  ```python
  print(xwalk[xwalk['2010 SOC Code'] == '43-9011'])
  ```

**Handling:**
- `13-1082`: genuine 3-source convergence (`11-9199` + `13-1199` + `15-1199`). No proportional weighting source available. **Documented limitation:** value duplicated/averaged equally across the three sources; true weighting would require BLS OEWS employment microdata, which this project does not have. Note that BLS's own 2019 OEWS hybrid occupation build used only `13-1199` + the project-management portion, explicitly excluding `11-9199` and `15-1199` as too small/noisy to include — this project's default (equal-weight) is more conservative than BLS's own precedent.
- All other codes in this cluster: standard 1:many split, duplicate source value, except `43-9011` which is a simple 1:1 absorption once confirmed.

### 2. First-Line Supervisors: Personal Service + Transportation

**Old codes:** `39-1021`, `53-1031`
**New codes:** `39-1014`, `39-1022`, `53-1043`, `53-1044`, `53-1049`

Confirmed via direct crosswalk row inspection: both `39-1021` and `53-1031`
map to `53-1044` (First-Line Supervisors of Passenger Attendants). This is
the genuine merge point — `53-1044`'s SOC definition ("Supervise and
coordinate activities of passenger attendants... includes supervisors of
Flight Attendants") plausibly draws from both personal-service and
transportation-supervisor populations.

**Handling:**
- `53-1044`: many:1 merge from `39-1021` + `53-1031`. Mean of both source values, documented as a cross-domain convergence.
- `39-1014`, `39-1022`: clean 1:many split from `39-1021` alone.
- `53-1043`, `53-1049`: clean 1:many split from `53-1031` alone.

### 3. Earth Drillers / Explosives Workers

**Old codes:** `47-5021`, `47-5031`
**New codes:** `47-5023`, `47-5032`

Titles are nearly identical to their old counterparts (`47-5023` "Earth
Drillers, Except Oil and Gas" = same title as old `47-5021`). This is
predominantly two parallel 1:1 renames. One row in the raw crosswalk showed
a small cross-mapping (`47-5021` → `47-5032`), suggesting a minor slice of
drillers-who-also-blast were reclassified into Explosives Workers.

**Handling:** treat as two parallel 1:1 continuations (`47-5021`→`47-5023`,
`47-5031`→`47-5032`) with a documented minor cross-contamination noted but
not separately modeled, given its likely small size.

### 4. Mathematical Technicians / Data Scientists

**Old codes:** `15-2091`, `15-2099`
**New codes:** `15-2051`, `15-2099`

The 2018 SOC Manual's Table 3 confirms `15-2051` (Data Scientists) is an
"All Other" breakout from `15-2099`, not derived from Mathematical
Technicians. `15-2091` appears to retire and fold into the continuing
`15-2099` catch-all.

**Handling:**
- `15-2099` (old) → `15-2051` (carve-out) + `15-2099` (narrower continuation): clean split.
- `15-2091` (old) → `15-2099` (absorbed): treat as merging into the continuation.

### 5. Engineering Technicians / Military Radar-Sonar Technicians

**Old codes:** `17-3029`, `55-3017`
**New codes:** `17-3028`, `17-3029`

Confirmed clean: `17-3029`'s (2018) own illustrative examples now list
"Radar Technicians, Sonar Technicians" — direct evidence the military code
`55-3017` folded into the continuing civilian catch-all. `17-3028`
(Calibration Technologists) is a separate, unrelated carve-out from the
same catch-all.

**Handling:**
- `17-3029` (old) → `17-3028` (carve-out) + `17-3029` (continuation): clean split.
- `55-3017` (old, military) → `17-3029` (continuation): treat as merge/absorption.
- Flag for team discussion: confirm whether military-origin codes should be in scope for this project at all.

### 6. Geological / Petroleum / Hydrologic Technicians

**Old codes:** `19-4041`, `19-4099`
**New codes:** `19-4043`, `19-4044`, `19-4099`

Clean: `19-4043` continues `19-4041`'s scope narrowed (petroleum-specific
portion split elsewhere or dropped). `19-4044` (Hydrologic Technicians) is
confirmed via Table 3 as an All-Other breakout from `19-4099`.

**Handling:** two independent 1:many splits, one from each old code.

### 7. Medical Records / Health Information Technologists

**Old codes:** `29-2071`, `29-9099`
**New codes:** `29-2072`, `29-9021`, `29-9093`, `29-9099`

`29-2072`'s (Medical Records Specialists) exclude clause explicitly names
`29-9021` (Health Information Technologists and Medical Registrars) as the
sibling split — same convergence pattern as `13-1082`.

**Handling:**
- `29-9021`: many:1 merge from `29-2071` + `29-9099` (technical/registrar-level work from both). Documented as equal-weight, same limitation as `13-1082`.
- `29-2072`: narrower continuation of `29-2071` (coding-focused work).
- `29-9093` (Surgical Assistants): clean carve-out from `29-9099`, unrelated to the health-information convergence.
- `29-9099`: narrower continuation.

### 8. Financial Analysts / Financial Risk Specialists

**Old codes:** `13-2051`, `13-2099`
**New codes:** `13-2051`, `13-2054`, `13-2099`

Likely two clean parallel transitions: `13-2051` old renames/expands to
`13-2051` new ("Financial and Investment Analysts"); `13-2099` old spawns
`13-2054` (Financial Risk Specialists) as a carve-out, continuing narrower
as `13-2099`. Lower confidence than other clusters — worth a second look if
time allows, but low risk given both plausible parent/child relationships
are clean 1:1 or 1:many.

**Handling:** treat as two independent transitions (rename + separate carve-out).

### 9. Health Technologists catch-all / Medical Dosimetrists

**Old codes:** `29-2054`, `29-2099`
**New codes:** `29-2036`, `29-2099`

Similar shape to cluster 8: `29-2036` (Medical Dosimetrists) is plausibly a
carve-out from the `29-2099` catch-all; `29-2054`'s exact fate is less
certain from definitions alone. Lower confidence, low risk.

**Handling:** treat as two independent transitions; flag as lower-confidence.

### 10. Machine Tool Operators / CNC Operators & Programmers

**Old codes:** `51-4011`, `51-4012`, `51-9199`
**New codes:** `51-9161`, `51-9162`, `51-9199`

`51-9161`/`51-9162` (CNC Tool Operators/Programmers) are new specific
breakouts. `51-9199`'s definition shows no exclude pointing at CNC work,
consistent with the CNC codes being carved primarily from the more general
machine-operator codes (`51-4011`/`51-4012`) rather than the catch-all.
Exact proportional contribution from each old code is not determinable from
definitions alone.

**Handling:** duplicate value across `51-9161`/`51-9162` from both
`51-4011` and `51-4012` (equal-weight), `51-9199` continues narrower.
Documented as a limitation — true split would need employment microdata.

### 11. Bus/Taxi Drivers → Shuttle Drivers, Bus Drivers, Taxi Drivers

**Old codes:** `53-3022`, `53-3041`
**New codes:** `53-3051`, `53-3053`, `53-3054`

`53-3054`'s (Taxi Drivers) exclude clause names `53-3053` (Shuttle
Drivers/Chauffeurs) as the sibling. Likely: `53-3022` (Bus Drivers, School
or Special Client) splits into `53-3051` (school bus, continuation) +
`53-3053` (special-client portion, feeds shuttle/chauffeur). `53-3041`
(Taxi Drivers and Chauffeurs) splits into `53-3053` (chauffeur portion) +
`53-3054` (taxi portion, continuation).

**Handling:**
- `53-3051`: continuation of `53-3022`'s school-bus portion.
- `53-3054`: continuation of `53-3041`'s taxi portion.
- `53-3053`: many:1 merge of the "special client" slice of `53-3022` and the "chauffeur" slice of `53-3041`. Equal-weight, documented limitation.

### 12. Excavating/Dragline Operators → Extraction Workers, All Other

**Old codes:** `53-7032`, `53-7199`
**New codes:** `47-5022`, `53-7199`

Cross-major-group reclassification (53-series Transportation into
47-series Extraction) — not verified against definitions in this pass.
**Flag for manual follow-up**: search `47-5022` and `53-7032` definitions
specifically before finalizing.

### 13. Mine Cutting/Channeling Machine Operators → Underground/Extraction catch-alls

**Old codes:** `47-5042`, `47-5049`, `47-5099`
**New codes:** `47-5049`, `47-5099`

`47-5042` (Mine Cutting and Channeling Machine Operators) was a narrow,
specific detailed occupation. Not independently verified against the
definitions PDF in this pass, but this fits the same "specific occupation
retires into an All Other catch-all" pattern seen repeatedly elsewhere in
this crosswalk (e.g., `43-9011`, `15-2091`).

**Handling (moderate confidence, pattern-based):** treat `47-5042` as
absorbed into `47-5049` (Underground Mining Machine Operators, All Other —
same major/minor group, most plausible destination). `47-5049` and
`47-5099` otherwise continue narrower. **Recommend a quick confirmation
search** on `47-5042`'s definition/exclude clause before finalizing, same
as cluster 12.

## Documented limitations (for coverage report)

The following codes have values duplicated/averaged across multiple
contributing sources without employment-weighting, since no weighting
source (e.g., BLS OEWS employment microdata) is available to this project:

- `13-1082` (3-way convergence)
- `29-9021` (2-way convergence)
- `53-1044` (2-way convergence)
- `51-9161`, `51-9162` (ambiguous proportional split)
- `53-3053` (2-way convergence)
- `47-5049` (pattern-based absorption of `47-5042`, not independently confirmed — verify before final submission)

These should be called out explicitly in the coverage report as a stated
methodological choice, not silently absorbed into the merged table.

## Outstanding action items before this document is considered final

1. Run the `43-9011` raw-row filter above and confirm its actual crosswalk target.
2. Search definitions for `47-5022`, `53-7032` (cluster 12) and `47-5042` (cluster 13) to move them from pattern-based inference to confirmed.
3. Clusters 8 and 9 (`13-2051`/`13-2099` and `29-2054`/`29-2099`) remain lower-confidence — worth a second pass if time allows.
