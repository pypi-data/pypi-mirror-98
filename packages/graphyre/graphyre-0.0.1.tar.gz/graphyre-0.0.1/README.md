# Graphyre

GraphQL API security testing tool

## Installation

### For Development

Requires Python 3.8 or greater. Make sure your `pip` is up to date.

```
python3 -m venv ./.venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements-dev.txt
```

## Features

### Inspect

- Detect allowed HTTP verbs.
- Detect maximum allowed batched queries.
- Detect maximum allowed nested queries.
- Gather intentionally triggered error messages.
- Run full a full introspectspection query.


