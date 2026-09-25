import pandas as pd
from datasets import load_dataset

DATASET = "Daudipdg/kenya-law-corpus"
REVISION = "8baca7e3b15afe9cb427b5adf8c851f889cc90fd"
SLICE_IDS = "../data/slice_chunk_ids.csv"


def load_case_law():
    """All case_law chunks at the pinned revision, with metadata flattened into columns."""
    raw = load_dataset(DATASET, revision=REVISION)["train"].to_pandas()
    meta = pd.json_normalize(raw["metadata"])
    df = pd.concat([raw.drop(columns="metadata"), meta], axis=1)
    return df[df["type"] == "case_law"].reset_index(drop=True)


def load_slice(case_law):
    """The frozen 400-chunk slice, in the order the IDs were saved."""
    ids = pd.read_csv(SLICE_IDS)["chunk_id"]
    return case_law.set_index("chunk_id").loc[ids].reset_index()


def page_only_urls(case_law):
    """Judgments where only the Kenya Law page header was scraped, not the judgment text."""
    has_marker = case_law.groupby("url")["text"].apply(lambda t: t.str.contains("Loading PDF").any())
    return set(has_marker[has_marker].index)


def clean_slice(df, case_law):
    """Apply the cleaning steps in order. Returns the cleaned frame and a before/after log."""
    log = []

    before = len(df)
    df = df[~df["url"].isin(page_only_urls(case_law))]
    log.append(("drop chunks from page-header-only judgments", before, len(df)))

    before = len(df)
    df = df.drop_duplicates(subset="text")
    log.append(("drop exact duplicate text", before, len(df)))

    df = df.copy()
    changed = (df["text"] != df["text"].str.strip()).sum()
    df["text"] = df["text"].str.strip()
    log.append((f"strip leading/trailing whitespace ({changed} chunks changed)", len(df), len(df)))

    changed = df["title"].str.contains("\xa0").sum()
    df["title"] = df["title"].str.replace("\xa0", " ")
    log.append((f"replace non-breaking spaces in title ({changed} titles changed)", len(df), len(df)))

    log = pd.DataFrame(log, columns=["step", "rows before", "rows after"])
    return df.reset_index(drop=True), log
