#!/usr/bin/env python3
import argparse
import csv
import json
from collections import defaultdict
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

REQUIRED_COLUMNS = {'order_id', 'customer_name', 'amount'}


def money(value: Decimal) -> float:
    return float(value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))


def summarize_csv(input_path: str):
    total_orders = 0
    total_revenue = Decimal('0')
    by_customer = defaultdict(lambda: Decimal('0'))

    with open(input_path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError('CSV file has no header row')
        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            raise ValueError(f'Missing required columns: {", ".join(sorted(missing))}')

        for line_no, row in enumerate(reader, start=2):
            customer = (row.get('customer_name') or '').strip()
            amount_raw = (row.get('amount') or '').strip()
            if not customer:
                raise ValueError(f'Line {line_no}: customer_name is empty')
            try:
                amount = Decimal(amount_raw)
            except InvalidOperation as exc:
                raise ValueError(f'Line {line_no}: invalid amount {amount_raw!r}') from exc
            total_orders += 1
            total_revenue += amount
            by_customer[customer] += amount

    top_5 = sorted(by_customer.items(), key=lambda item: (-item[1], item[0]))[:5]
    return {
        'total_orders': total_orders,
        'total_revenue': money(total_revenue),
        'top_5_customers': [
            {'customer_name': name, 'total_amount': money(total)} for name, total in top_5
        ],
    }


def main():
    parser = argparse.ArgumentParser(description='Summarize CSV sales data into JSON')
    parser.add_argument('--input', required=True, help='Input CSV file')
    parser.add_argument('--output', required=True, help='Output JSON file')
    args = parser.parse_args()

    summary = summarize_csv(args.input)
    Path(args.output).write_text(json.dumps(summary, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
