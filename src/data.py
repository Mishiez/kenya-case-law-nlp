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
