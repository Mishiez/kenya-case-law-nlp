# Labelling guide

Rules for hand-labelling the 20 evaluation chunks. They were written **before** labelling and are not changed afterwards, so the baseline is scored against a fixed definition of each entity, not one adjusted to fit what it happens to find.

## What to label

Label only the chunk text, not the judgment title shown above it. Copy each entity **exactly as written**, including odd spacing and punctuation. Whitespace differences and letter case are ignored when scoring.

### DATE
A calendar date with **day, month and year**, in any format.

| Label | Don't label |
|---|---|
| `26/6/2025` | `2025` (year only) |
| `25th March, 2026` | `March 2026` (no day) |
| `13 th August 2016` | `the 3 rd defendant` (an ordinal, not a date) |
| `23 RD DAY OF MARCH, 2026` | `1100hours` (time) |

### MONEY
An amount in **Kenyan shillings**, written in figures or words. Include the currency marker and any `/=` or cents.

| Label | Don't label |
|---|---|
| `Kshs. 80,000/=` | amounts in other currencies |
| `Sh. 50,000` | `[2017] KESC 2` (a court code) |
| `Kenya Shillings One Million` | `3 cows` |
| `Kshs 4, 000` | |

If a chunk gives the same amount in words and in figures, e.g. `Kenya Shillings One Million (Kshs. 1,000,000/=)`, label them as two separate entities.

### CASE_REF
A reference that identifies a **court case**: a case number or a law-report citation. Include the full case type as written.

| Label | Don't label |
|---|---|
| `Civil Appeal No. E031 of 2023` | `Land Act No. 6 of 2012` (a statute) |
| `Environment & Land Case E018 of 2025` | `Section 26(1)` (a provision) |
| `[2026] KEHC 3922 (KLR)` | party names on their own, e.g. `Mwangi v Republic` |
| `[2018] eKLR`, `[1974] EA 75` | |

For a case name followed by a citation, such as `Mwangi v Republic [2026] KEHC 3922 (KLR)`, label only the citation part.

## Edge cases

- **Cut off at the chunk edge:** if the entity is still recognisable, label the part that's visible (e.g. a chunk ending `Civil Appeal No. E0`). If it can't be recognised, skip it.
- **Repeats:** if the same entity appears twice in a chunk, label it twice.
- **Unsure:** label it, and add a note in the entry (see below). Borderline cases are useful in the failure analysis.

## Format

Write the labels in `data/labels.csv`, one row per entity:

```
item,type,text,note
L01,DATE,26/6/2025,
L02,CASE_REF,Land Case E018 of 2025,
L02,MONEY,"Kshs. 80,000/=",
L05,DATE,23 rd January 2025,spaced ordinal
```

Put `text` in double quotes if it contains a comma. `note` is optional. A chunk with no entities gets no rows. That's fine: the item list in `data/eval_sample.csv` records that it was checked.
