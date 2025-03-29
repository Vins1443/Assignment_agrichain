import unittest

class Checkout:
    def __init__(self, pricing_rules):
        self.pricing_rules = pricing_rules
        self.items = {}
    
    def scan(self, item):
        if item in self.items:
            self.items[item] += 1
        else:
            self.items[item] = 1
    
    def total(self):
        total_price = 0
        for item, quantity in self.items.items():
            price, discount_qty, discount_price = self.pricing_rules[item]
            if discount_qty:
                total_price += (quantity // discount_qty) * discount_price + (quantity % discount_qty) * price
            else:
                total_price += quantity * price
        return total_price

class TestCheckout(unittest.TestCase):
    def setUp(self):
        self.pricing_rules = {
            'A': (50, 3, 130),  # (Unit price, Discount quantity, Discount price)
            'B': (30, 2, 45),
            'C': (20, None, None),
            'D': (15, None, None)
        }
        self.checkout = Checkout(self.pricing_rules)
    
    def test_empty_cart(self):
        self.assertEqual(self.checkout.total(), 0)
    
    def test_single_item(self):
        self.checkout.scan('A')
        self.assertEqual(self.checkout.total(), 50)
    
    def test_multiple_items_no_discount(self):
        self.checkout.scan('A')
        self.checkout.scan('B')
        self.assertEqual(self.checkout.total(), 80)
    
    def test_multiple_items_with_discount(self):
        self.checkout.scan('A')
        self.checkout.scan('A')
        self.checkout.scan('A')
        self.assertEqual(self.checkout.total(), 130)
    
    def test_mixed_items_with_discounts(self):
        for item in "AAABB":
            self.checkout.scan(item)
        self.assertEqual(self.checkout.total(), 175)
    
    def test_mixed_order_scanning(self):
        for item in "DABABA":
            self.checkout.scan(item)
        self.assertEqual(self.checkout.total(), 190)

if __name__ == "__main__":
    # Sample test case print statement
    pricing_rules = {
        'A': (50, 3, 130),  # (Unit price, Discount quantity, Discount price)
        'B': (30, 2, 45),
        'C': (20, None, None),
        'D': (15, None, None)
    }
    checkout = Checkout(pricing_rules)
    for item in "DABABA":
        checkout.scan(item)
    print(f"Total price for AABBCD: {checkout.total()}")
    
    unittest.main()
