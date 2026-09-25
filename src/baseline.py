import re

MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"

# One simple pattern per format seen in the EDA. No ML, no context, no special cases.
PATTERNS = {
    "DATE": {
        "numeric":       rf"\b\d{{1,2}}[/.-]\d{{1,2}}[/.-](?:\d{{4}}|\d{{2}})\b",            # 13/7/2022
        "day_month":     rf"\b\d{{1,2}}(?:st|nd|rd|th)?\s+(?:{MONTHS}),?\s+\d{{4}}\b",      # 25th March 2026
        "month_day":     rf"\b(?:{MONTHS})\s+\d{{1,2}},?\s+\d{{4}}\b",                        # March 25, 2026
    },
    "MONEY": {
        "kes":           r"\b(?:KES|Kshs?|KSh)\.?\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?(?:/=)?",   # Kshs. 80,000/=
    },
    "CASE_REF": {
        "case_number":   r"\b(?:Civil|Criminal|Succession|Petition|Appeal|Application|Case|Cause|Suit)\b"
                         r"[A-Za-z .&]{0,40}?(?:No\.?\s*)?E?\d+\s+of\s+\d{4}\b",               # Civil Appeal No. 27 of 2010
        "neutral":       r"\[\d{4}\]\s+(?:eKLR|[A-Z]+\s+\d+(?:\s+\(KLR\))?)",                  # [2026] KEHC 3922 (KLR)
    },
}


def extract(text):
    """Every match in the text as a dict with entity type, pattern name, matched string and position."""
    found = []
    for entity, patterns in PATTERNS.items():
        for name, pattern in patterns.items():
            for m in re.finditer(pattern, text, flags=re.IGNORECASE):
                found.append({
                    "type": entity,
                    "pattern": name,
                    "text": m.group(),
                    "start": m.start(),
                    "end": m.end(),
                })
    return sorted(found, key=lambda e: e["start"])
