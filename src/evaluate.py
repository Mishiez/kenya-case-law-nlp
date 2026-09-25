import re

import pandas as pd

from baseline import extract

SEED = 42
N_WITH_MATCHES = 12
N_WITHOUT_MATCHES = 8


def select_eval_sample(df):
    """Chunks to hand-label: some where the baseline fired, some where it found nothing."""
    has_match = df["text"].apply(lambda t: len(extract(t)) > 0)
    with_matches = df[has_match].sample(n=N_WITH_MATCHES, random_state=SEED)
    without = df[~has_match].sample(n=N_WITHOUT_MATCHES, random_state=SEED)

    sample = pd.concat([with_matches, without]).reset_index(drop=True)
    sample.insert(0, "item", [f"L{i:02d}" for i in range(1, len(sample) + 1)])
    sample["baseline_fired"] = [True] * N_WITH_MATCHES + [False] * N_WITHOUT_MATCHES
    return sample


def gold_spans(sample, labels):
    """Turn each hand label into (item, type, start, end) by finding it in the chunk text."""
    rows = []
    for (item, entity, text), group in labels.groupby(["item", "type", "text"]):
        chunk = sample.loc[sample["item"] == item, "text"].iloc[0]
        pattern = r"\s+".join(re.escape(word) for word in text.split())
        for m in re.finditer(pattern, chunk, flags=re.IGNORECASE):
            rows.append({"item": item, "type": entity, "text": m.group(), "start": m.start(), "end": m.end()})
    return pd.DataFrame(rows)


def predicted_spans(sample):
    """Baseline predictions for every chunk in the sample."""
    rows = [{"item": r.item, **e} for r in sample.itertuples() for e in extract(r.text)]
    return pd.DataFrame(rows).drop(columns="pattern")


def match(gold, pred, mode):
    """Pair each prediction with at most one gold span of the same type in the same chunk.

    mode="exact":   start and end must both be equal
    mode="partial": the spans only need to overlap
    """
    gold = gold.assign(matched=False)
    pred = pred.assign(matched=False)
    for i, p in pred.iterrows():
        candidates = gold[(gold["item"] == p["item"]) & (gold["type"] == p["type"]) & ~gold["matched"]]
        if mode == "exact":
            hit = candidates[(candidates["start"] == p["start"]) & (candidates["end"] == p["end"])]
        else:
            hit = candidates[(candidates["start"] < p["end"]) & (candidates["end"] > p["start"])]
        if len(hit):
            gold.loc[hit.index[0], "matched"] = True
            pred.loc[i, "matched"] = True
    return gold, pred


def score(gold, pred, mode):
    """Precision, recall and F1 per entity type, plus an overall row."""
    gold, pred = match(gold, pred, mode)
    rows = []
    for entity in ["DATE", "MONEY", "CASE_REF", "ALL"]:
        g = gold if entity == "ALL" else gold[gold["type"] == entity]
        p = pred if entity == "ALL" else pred[pred["type"] == entity]
        tp = p["matched"].sum()
        fp = len(p) - tp
        fn = len(g) - g["matched"].sum()
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        rows.append({"type": entity, "gold": len(g), "predicted": len(p), "TP": tp, "FP": fp, "FN": fn,
                     "precision": round(precision, 2), "recall": round(recall, 2), "F1": round(f1, 2)})
    return pd.DataFrame(rows).set_index("type")
