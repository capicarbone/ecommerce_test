from decimal import Decimal
import unittest

from products_storage import ProductsStorage
from utils import create_fake_products_storage

class ProductsStorageTest(unittest.TestCase):

    def setUp(self) -> None:
        self.storage = create_fake_products_storage()
    

    def test_is_valid_region(self):        

        self.assertTrue(self.storage.is_valid_region('es'))
        self.assertTrue(self.storage.is_valid_region('eS'))
        self.assertFalse(self.storage.is_valid_region('xx'))

    def test_add_product(self):

        new_sku = "ps5"
        self.storage.add_product("ps5", "Playstation 5")

        new_product = self.storage._products.get(new_sku, None)

        self.assertIsNotNone(new_product)
        self.assertEqual(new_sku, new_product.sku)

    def test_add_region_to_product(self):
        new_sku = "ps5"
        self.storage.add_product("ps5", "Playstation 5")

        self.storage.add_region_to_product(new_sku, 'es', Decimal("12.00"), Decimal("0.2"))

        new_product = self.storage._products[new_sku]
        
        self.assertIn('es', new_product.regions)

    def test_get_products(self):

        p = self.storage.get_product('ps4')

        self.assertIsNotNone(p)
        self.assertEqual(p.sku, 'ps4')


