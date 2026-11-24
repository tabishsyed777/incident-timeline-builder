# Incident Timeline Builder

Reconstruct an incident from unordered timestamped evidence. Normalize offsets to UTC, cite every event and measure elapsed time between the first and last observations.

## Quick start

From this directory, run these commands with Python 3.12 or 3.13. The example corpus is fictional and runs offline with the standard library.

```sh
python3 core.py ask 'Timeline for atlas'
python3 core.py build data/source.json snapshot.json
python3 core.py ask 'First event for atlas' --snapshot snapshot.json
python3 -m unittest discover -v
python3 evaluate.py
```

## Asking questions

Ask “Timeline for atlas”, “First event for atlas”, “Last event for atlas”, or “Elapsed time for atlas”.

## Using your own sources

Use the records in `data/source.json` as a schema example. Supply unique citation IDs and usable source locators. Build a new snapshot after additions, edits, or deletions. A successful build atomically replaces the previous snapshot. Results contain the answer, retrieval method and source locators. Unsupported queries return `insufficient_evidence`.

Events must already be assigned an incident ID. Equal timestamps are ordered by evidence ID. Elapsed time measures the observation window and does not establish downtime or causality.

See [QA.md](QA.md) for measured results, review status and release limits.
