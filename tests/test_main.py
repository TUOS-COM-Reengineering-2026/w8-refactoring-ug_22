import unittest
import io
import contextlib

from main import CustomerManager, calculate_shipping_fee_for_fragile_items, calculate_shipping_fee_for_heavy_items

class TestCustomerManager(unittest.TestCase):

    def test_add_customer(self):
        cm = CustomerManager()
        name = "Alice"
        purchases = [{'price': 50, 'item': 'banana'}, {'price': 80, 'item': 'apple'}]
        cm.add_customer(name, purchases)

        self.assertEqual(
            {name: purchases},
            cm.customers
        )

    def test_add_purchase(self):
        cm = CustomerManager()
        name = "Alice"
        purchase = {'price': 50, 'item': 'banana'}
        cm.add_purchase(name, purchase)

        self.assertEqual(
            {name: [purchase]},
            cm.customers
        )

    def test_add_purchases(self):

        cm = CustomerManager()
        name = "Alice"
        purchases = [{'price': 50, 'item': 'banana'}, {'price': 200, 'item': 'apple'}]
        cm.add_purchases(name, purchases)

        self.assertEqual(
            {name: [{'price': 50, 'item': 'banana'}, {'price': 200, 'item': 'apple'}]},
            cm.customers
        )

    def test_calculate_shipping_fee_for_heavy_items_when_less_than_twenty(self):

        purchases = [{'price': 50, 'item': 'banana'}, {'price': 200, 'item': 'apple', "weight": 0}]
        actual = calculate_shipping_fee_for_heavy_items(purchases)
        self.assertEqual(20, actual)

    def test_calculate_shipping_fee_for_heavy_items_when_more_than_twenty(self):

        purchases = [{'price': 50, 'item': 'banana'}, {'price': 200, 'item': 'apple', "weight": 100}]
        actual = calculate_shipping_fee_for_heavy_items(purchases)
        self.assertEqual(50, actual)


    def test_add_purchase_multiple(self):
        cm = CustomerManager()
        name = "Alice"
        purchase = {'price': 50, 'item': 'banana'}
        cm.add_purchase(name, purchase)
        cm.add_purchase(name, purchase)

        self.assertEqual(
            {name: [purchase, purchase]},
            cm.customers
        )

    def test_discount_eligibility(self):
        cm = CustomerManager()
        cm.add_customer("Bob", [{'price': 600}])

        # Capture printed output
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()

        self.assertIn("Bob", output)
        self.assertIn("Eligible for discount", output)

    def test_generate_report_below_tax_threshold(self):
        cm = CustomerManager()
        cm.add_customer("Bob", [{'price': 50}])

        # Capture printed output
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()

        self.assertIn("Bob", output)
        self.assertIn("No discount", output)

    def test_generate_report_above_tax_threshold_below_discount(self):
        cm = CustomerManager()
        cm.add_customer("Bob", [{'price': 400}])

        # Capture printed output
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()

        self.assertIn("Bob", output)
        self.assertIn("Potential future discount customer", output)

    def test_generate_report_vip(self):
        cm = CustomerManager()
        cm.add_customer("Bob", [{'price': 1200}])

        # Capture printed output
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()

        self.assertIn("Bob", output)
        self.assertIn("VIP Customer!", output)

    def test_generate_report_priority_customer(self):
        cm = CustomerManager()
        cm.add_customer("Bob", [{'price': 800}])

        # Capture printed output
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()

        self.assertIn("Bob", output)
        self.assertIn("Priority Customer", output)

    def test_heavy_item_shipping_fee(self):
        cm = CustomerManager()
        purchases = [{'price': 100, 'weight': 25}]

        fee = cm.calculate_shipping_fee(purchases)
        self.assertEqual(fee, 50)

    def test_fragile_item_shipping_fee(self):
        purchases = [{'price': 70, 'fragile': True}]

        fee = calculate_shipping_fee_for_fragile_items(purchases)
        self.assertEqual(fee, 60)

    def test_no_special_items_shipping_fee(self):
        cm = CustomerManager()
        purchases = [{'price': 40, 'weight': 5, 'fragile': False}]

        fee = cm.calculate_shipping_fee(purchases)
        self.assertEqual(fee, 20)

        fee_fragile = calculate_shipping_fee_for_fragile_items(purchases)
        self.assertEqual(fee_fragile, 25)

if __name__ == "__main__":
    unittest.main()
