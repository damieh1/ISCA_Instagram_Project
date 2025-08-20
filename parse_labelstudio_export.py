""""
---------------------------------
|WORK IN PROGRESS :-)           |
---------------------------------
Parse a Label Studio JSON export (for image classification project) into a tidy pandas DataFrame.

Works with the labeling config that includes the following controls:
- emotional_content (single choice)
- text_present (single choice)
- scene_types (multiple choice)
- support_for_terror (single choice)
- stance_target (multiple choice, optional)
- emotion_impact (rating, 1..7)
- dominant_emotion (single choice)
- transcribed_text (textarea)
- notes (textarea)

USAGE
-----
python parse_labelstudio_export.py /path/to/export.json --out /path/to/output.csv

OPTIONS
-------
--explode-multi True/False : explode multi-select fields into long rows (default False)
--one-hot True/False       : add one-hot columns for multi-select fields (default False)

The script can also be imported and used via parse_labelstudio_to_df(export_json_path, ...).
"""

from __future__ import annotations
import argparse
import json
from typing import Any, Dict, List, Optional, Tuple, Iterable
import pandas as pd
from pathlib import Path

# Controls expected in config
SINGLE_CHOICE_FIELDS = {"emotional_content", "text_present", "support_for_terror", "dominant_emotion"}
MULTI_CHOICE_FIELDS  = {"scene_types", "stance_target"}
RATING_FIELDS        = {"emotion_impact"}
TEXTAREA_FIELDS      = {"transcribed_text", "notes"}

ALL_FIELDS = list(SINGLE_CHOICE_FIELDS | MULTI_CHOICE_FIELDS | RATING_FIELDS | TEXTAREA_FIELDS)

def _safe_get(d: dict, *keys, default=None):
    cur = d
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur

def _result_to_values(res: dict) -> Tuple[str, Any]:
    field = res.get("from_name")
    rtype = res.get("type")
    value = res.get("value", {})

    if rtype == "choices":
        choices = value.get("choices", [])
        return field, list(choices)  # keep list even for single-choice
    elif rtype == "rating":
        return field, value.get("rating")
    elif rtype == "textarea":
        texts = value.get("text", [])
        joined = "\n".join([t for t in texts if isinstance(t, str)])
        return field, joined
    else:
        # Unknown/unsupported type — keep raw
        return field, value

def _annotation_to_record(task: dict, ann: dict) -> dict:
        #Flatten a single annotation into a record.
    record = {
        "task_id": task.get("id"),
        "annotation_id": ann.get("id"),
        "project": task.get("project"),
        "image": _safe_get(task, "data", "image"),
        "annotator_id": _safe_get(ann, "completed_by", "id") or ann.get("completed_by"),
        "annotator_username": _safe_get(ann, "completed_by", "email") or _safe_get(ann, "completed_by", "username"),
        "created_at": ann.get("created_at"),
        "updated_at": ann.get("updated_at"),
        "lead_time": ann.get("lead_time"),
        # Defaults for all expected fields
        **{f: None for f in ALL_FIELDS},
    }

    results: List[dict] = ann.get("result") or []
    # not yet tested
    if not results and "results" in ann:
        results = ann["results"]

    for res in results:
        field, val = _result_to_values(res)
        if not field:
            continue

        if field in MULTI_CHOICE_FIELDS:
            # ensure list
            if isinstance(val, list):
                record[field] = val
            elif val is None:
                record[field] = []
            else:
                record[field] = [val]
        elif field in SINGLE_CHOICE_FIELDS:
            # pick first if list
            if isinstance(val, list):
                record[field] = val[0] if val else None
            else:
                record[field] = val
        elif field in RATING_FIELDS:
            record[field] = val
        elif field in TEXTAREA_FIELDS:
            record[field] = val
        else:
            # unknown control; store as-is
            record[field] = val

    return record

def _iter_records(tasks: Iterable[dict]) -> Iterable[dict]:
    for t in tasks:
        annotations = t.get("annotations") or []
        # Some exports may use 'completions' (legacy)
        if not annotations and "completions" in t:
            annotations = t["completions"]
        if not annotations:
            # produce an empty "annotation" record with task metadata only
            yield {
                "task_id": t.get("id"),
                "annotation_id": None,
                "project": t.get("project"),
                "image": _safe_get(t, "data", "image"),
                **{f: None for f in ALL_FIELDS},
            }
            continue

        for ann in annotations:
            yield _annotation_to_record(t, ann)

def _one_hot_multi(df: pd.DataFrame, fields: List[str]) -> pd.DataFrame:
    df = df.copy()
    for f in fields:
        # Gather unique values
        unique_vals = sorted({v for lst in df[f].dropna().tolist() for v in (lst if isinstance(lst, list) else [])})
        for u in unique_vals:
            col = f"{f}__{u}".replace(" ", "_").replace("/", "_").replace("-", "_").replace("(", "").replace(")", "")
            df[col] = df[f].apply(lambda x: int(isinstance(x, list) and (u in x)))
    return df

def _explode_multi(df: pd.DataFrame, fields: List[str]) -> pd.DataFrame:
    df = df.copy()
    for f in fields:
        df[f] = df[f].apply(lambda v: v if isinstance(v, list) and v else [None])
        df = df.explode(f, ignore_index=True)
    return df

def parse_labelstudio_to_df(
    export_json_path: str | Path,
    explode_multi: bool = False,
    one_hot: bool = False
) -> pd.DataFrame: # Load a Label Studio JSON export and convert to a tidy DataFrame.
        p = Path(export_json_path)
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Exports can be dict {"tasks": [...]} or list of tasks
    tasks = data.get("tasks") if isinstance(data, dict) else data
    if tasks is None:
        raise ValueError("Could not find tasks in the export JSON. Expected a list or a dict with key 'tasks'.")

    records = list(_iter_records(tasks))
    df = pd.DataFrame.from_records(records)

    # Normalize types
    if "emotion_impact" in df.columns:
        df["emotion_impact"] = pd.to_numeric(df["emotion_impact"], errors="coerce")

    # Ensure lists for multi fields (for empty annotations)
    for f in MULTI_CHOICE_FIELDS:
        if f in df.columns:
            df[f] = df[f].apply(lambda x: x if isinstance(x, list) else ([] if pd.isna(x) else [x]))

    if explode_multi:
        df = _explode_multi(df, sorted(MULTI_CHOICE_FIELDS))

    if one_hot:
        df = _one_hot_multi(df, sorted(MULTI_CHOICE_FIELDS))

    return df

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("export_json", help="Path to Label Studio JSON export")
    ap.add_argument("--out", default="", help="Optional CSV output path")
    ap.add_argument("--explode-multi", default="False", help="Explode multi-select fields into long rows (True/False)")
    ap.add_argument("--one-hot", default="False", help="Add one-hot columns for multi-select fields (True/False)")
    args = ap.parse_args()

    explode_multi = args.explode_multi.lower() == "true"
    one_hot = args.one_hot.lower() == "true"

    df = parse_labelstudio_to_df(args.export_json, explode_multi=explode_multi, one_hot=one_hot)
    if args.out:
        df.to_csv(args.out, index=False)
        print(f"Saved CSV → {args.out}")
    else:
        # Pretty print a small sample
        with pd.option_context("display.max_columns", None, "display.width", 160):
            print(df.head(10))

if __name__ == "__main__":
    main()

