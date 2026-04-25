import json
import tempfile
import unittest
from pathlib import Path

from main import summarize_csv, main


class CsvSummaryTests(unittest.TestCase):
    def test_summary_totals_and_top_customers(self):
        result = summarize_csv('sample.csv')
        self.assertEqual(result['total_orders'], 7)
        self.assertEqual(result['total_revenue'], 1178.10)
        self.assertEqual(result['top_5_customers'][0], {'customer_name': 'Dora', 'total_amount': 500.10})
        self.assertEqual(result['top_5_customers'][1], {'customer_name': 'Alice', 'total_amount': 400.75})
        self.assertEqual(result['top_5_customers'][2], {'customer_name': 'Bob', 'total_amount': 225.00})

    def test_missing_column_raises(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'bad.csv'
            p.write_text('order_id,customer_name\n1,Alice\n', encoding='utf-8')
            with self.assertRaises(ValueError):
                summarize_csv(str(p))

    def test_invalid_amount_raises(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'bad.csv'
            p.write_text('order_id,customer_name,amount\n1,Alice,nope\n', encoding='utf-8')
            with self.assertRaises(ValueError):
                summarize_csv(str(p))


if __name__ == '__main__':
    unittest.main()
