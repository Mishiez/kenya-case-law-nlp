# kenya-case-law-nlp

Exploring Kenyan case-law text through data analysis, cleaning, and a simple baseline for legal information extraction, as part of an AI legal case intelligence capstone (Track M, checkpoint M2.1).

The question: **how far does a deliberately naive, regex-only extractor get at pulling dates, Kenyan-shilling amounts and case references out of real Kenyan judgments, and where does it fail?**

## Results at a glance

Scored against 37 hand-labelled entities in 20 chunks (exact span match):

| Entity | Precision | Recall | F1 |
|---|---|---|---|
| DATE | 1.00 | 0.64 | 0.78 |
| MONEY | 0.83 | 0.71 | 0.77 |
| CASE_REF | 0.58 | 0.37 | 0.45 |
| **All** | **0.76** | **0.51** | **0.61** |

The baseline is accurate when it matches but misses about half the entities. The failures are systematic:
- **Spaced ordinals** such as `24 th February 2025` and `23 RD DAY OF MARCH, 2026` account for every missed date.
- **Law-report citations** outside the `[YYYY] CODE N` shape (`[2003] 2 EA 519`, `[1972] ALL ER 606`) are missed.
- **Wrong amounts can look right**: `Kshs 4, 000` is extracted as `Kshs 4`.

These are small-sample estimates; see [notebooks/06_failure_analysis.ipynb](notebooks/06_failure_analysis.ipynb) for the limitations.

## Dataset

[`Daudipdg/kenya-law-corpus`](https://huggingface.co/datasets/Daudipdg/kenya-law-corpus) on Hugging Face: legislation and judgments scraped from [new.kenyalaw.org](https://new.kenyalaw.org), split into chunks of up to 800 characters.

- **Version:** pinned to revision `8baca7e3b15afe9cb427b5adf8c851f889cc90fd`
- **Subset:** `case_law` only (17,353 chunks from 990 judgments), then a 400-chunk random sample (seed 42)
- **After cleaning:** 381 chunks from 253 judgments
- **Licence:** listed on the dataset card as not yet finalised. For that reason this repo stores only chunk IDs and short labelled entities, never judgment text. The data is re-downloaded at the pinned revision when the notebooks run.

**Data-quality finding:** 348 of the 990 judgments (35%) contain only the Kenya Law web-page header, not the judgment itself. The cleaning step removes these.

## Repository layout

```
notebooks/
  01_dataset_scope.ipynb      load, filter to case law, freeze the 400-chunk slice
  02_eda.ipynb                overview, missing values, duplicates, text length, pattern frequency
  03_cleaning.ipynb           cleaning steps with before/after counts
  04_baseline.ipynb           the regex baseline and its output
  05_evaluation.ipynb         hand labels, precision / recall / F1 per entity type
  06_failure_analysis.ipynb   failure cases, limitations, what this means for the capstone
src/
  data.py                     load the corpus, rebuild the slice, clean it
  baseline.py                 the regex patterns and extract()
  evaluate.py                 evaluation sample selection and scoring
data/
  slice_chunk_ids.csv         the frozen 400-chunk slice (IDs only)
  eval_sample.csv             the 20 chunks used for evaluation
  labels.csv                  hand labels for those 20 chunks
docs/
  scope.md                    dataset scope, subset and limitations
  labelling_guide.md          the rules used for hand-labelling
```

## Running it

Requires Python 3.12.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name m21-capstone --display-name "Python (M2.1 Capstone)"
jupyter lab
```

Run the notebooks in order from the `notebooks/` folder with the "Python (M2.1 Capstone)" kernel. The first run downloads the dataset (about 75 MB) from Hugging Face.

## Branches

Each phase was built on its own branch and merged into `main`:

| Branch | Phase |
|---|---|
| `setup/dataset-scope` | load, filter, freeze the slice, scope doc |
| `feature/eda-cleaning` | EDA and cleaning |
| `feature/baseline-extraction` | regex baseline |
| `feature/evaluation` | hand labels, scoring, failure cases, conclusions |
