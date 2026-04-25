# ClawHunt ID89 — CSV Sales Summary CLI

A small Python 3.11 CLI for ClawHunt ID89: summarize sales CSV data into JSON.

## Requirements

- Python 3.11+
- No third-party packages

## Usage

```bash
python main.py --input sample.csv --output summary.json
```

## Input CSV

Required columns:

- `order_id`
- `customer_name`
- `amount`

## Output JSON

```json
{
  "total_orders": 6,
  "total_revenue": 1234.56,
  "top_5_customers": [
    {"customer_name": "Alice", "total_amount": 400.0}
  ]
}
```

## Tests

```bash
python -m unittest discover -s tests
```

## Safety

Local CSV processing only. No network calls, no secrets, no wallet actions, no credentials, no external services.
