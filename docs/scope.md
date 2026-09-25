# Dataset scope — M2.1 checkpoint

## Dataset

| | |
|---|---|
| **Name** | Kenya Law Corpus (`Daudipdg/kenya-law-corpus` on Hugging Face) |
| **Revision used** | `8baca7e3b15afe9cb427b5adf8c851f889cc90fd` (last modified 2026-07-01) |
| **Source** | Legislation and judgments scraped from [new.kenyalaw.org](https://new.kenyalaw.org), the site of Kenya Law (National Council for Law Reporting). Documents are identified by Akoma Ntoso (AKN) URLs. |
| **Licence** | Listed as `other`. The card says the licence is *"not yet finalized — placeholder only"*. The underlying judgments are public record. |

## Contents

63,603 text chunks with 3 top-level columns:

- `chunk_id`: the source document's AKN URL plus a `##chunkN` suffix
- `text`: the passage, at most 800 characters
- `metadata`: a nested object holding `title`, `url`, `type`, `chunk_index`, `total_chunks`, `citation`, `court` and `date`

| `type` | Chunks |
|---|---|
| legislation | 46,250 |
| case_law | 17,353 |

## Subset used

1. **Filter:** `type == "case_law"` gives 17,353 chunks from 990 distinct judgments. The judgment dates that are filled in run from September 2024 to April 2026.
2. **Slice:** a simple random sample of **400 chunks** (`pandas.DataFrame.sample`, `random_state=42`).
3. **Frozen as:** [`data/slice_chunk_ids.csv`](../data/slice_chunk_ids.csv). Only the IDs are stored, not the text, because the licence is not finalised. Together with the pinned revision, the IDs rebuild the exact slice. [`notebooks/01_dataset_scope.ipynb`](../notebooks/01_dataset_scope.ipynb) checks this.

**What the slice contains:** 400 chunks from 272 judgments. 22 of them are the opening chunk of a judgment (title, parties, court). 26 are shorter than 800 characters.

| Court (from URL) | Chunks in slice |
|---|---|
| `kemc` Magistrates' Courts | 266 |
| `kehc` High Court | 42 |
| `keelc` Environment & Land Court | 37 |
| `kekc` Kadhis' Courts | 23 |
| `keca` Court of Appeal | 16 |
| `keelrc` Employment & Labour Relations Court | 16 |
| `kesc` Supreme Court | 0 |

## Limitations

- **The unit is a chunk, not a judgment.** Text is cut at a fixed 800 characters, often mid-sentence or mid-word. A date, amount or case reference can be split across two chunks, so neither chunk contains the whole entity.
- **Metadata is thin.** `citation` and `court` are empty on every case-law row, and `date` is empty on 727. Court has to be parsed from the URL.
- **The slice is skewed towards Magistrates' Courts** (67%), with no Supreme Court chunks. That mirrors the corpus, not Kenyan case law as a whole.
- **Narrow time window.** It covers only about 18 months of judgments (2024–2026), not a historical archive.
- **No ground-truth labels.** Any extraction scores depend on a small, hand-labelled sample from this slice.
- **Personal data.** Judgments name real litigants, and succession and family matters can name minors. The data is used here for research only.
- **Licence is unresolved**, which is why no text is committed.
- **Duplicates are not removed yet.** They are handled in the cleaning phase, where before/after counts are reported.

## Relevance to the capstone

The capstone is a legal case-intelligence system for Kenyan lawyers. The basic job is pulling structured facts out of judgments: **dates** (hearing, delivery, offence), **monetary amounts** (KES awards, fines, bail) and **case references** (for example *Civil Appeal No. X of YYYY*, neutral citations such as `[2025] KEMC 94 (KLR)`). This corpus is real Kenyan judgment text in the formats lawyers read. That makes it the right data for measuring how far a deliberately naive, regex-only extractor gets, and where it fails.
