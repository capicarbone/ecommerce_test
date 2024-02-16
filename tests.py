from decimal import Decimal
import unittest

from products_storage import ProductsStorage
from shopping_cart import PromoCode, ShoppingCart, ShoppingCartItem
from utils import create_fake_products_storage


class ProductsStorageTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.storage = create_fake_products_storage()

    def test_is_valid_region(self):

        self.assertTrue(self.storage.is_valid_region("es"))
        self.assertTrue(self.storage.is_valid_region("eS"))
        self.assertFalse(self.storage.is_valid_region("xx"))

    def test_add_product(self):

        new_sku = "ps5"
        self.storage.add_product("ps5", "Playstation 5")

        new_product = self.storage._products.get(new_sku, None)

        self.assertIsNotNone(new_product)
        self.assertEqual(new_sku, new_product.sku)

    def test_add_region_to_product(self):
        new_sku = "ps5"
        self.storage.add_product("ps5", "Playstation 5")

        self.storage.add_region_to_product(
            new_sku, "es", Decimal("12.00"), Decimal("0.2")
        )

        new_product = self.storage._products[new_sku]

        self.assertIn("es", new_product.regions)

    def test_get_products(self):

        p = self.storage.get_product("PRODA")

        self.assertIsNotNone(p)
        self.assertEqual(p.sku, "PRODA")


class ShoppingCartItemTestCase(unittest.TestCase):

    def test_get_total_without_discount_for_one_item(self):

        sci = ShoppingCartItem(
            qty=1, sku="sss", description="test", unit_price=Decimal("200.00")
        )

        self.assertEqual(Decimal("200.00"), sci.total)

    def test_get_total_without_discount_for_many_items(self):

        sci = ShoppingCartItem(
            qty=5, sku="sss", description="test", unit_price=Decimal("200.00")
        )

        self.assertEqual(Decimal("1000.00"), sci.total)

    def test_get_total_with_discount_for_one_item(self):

        sci = ShoppingCartItem(
            qty=1,
            sku="sss",
            description="test",
            unit_price=Decimal("200.00"),
            discount=Decimal("0.2"),
        )

        self.assertEqual(Decimal("160.00"), sci.total)

    def test_get_total_with_discount_for_many_item(self):

        sci = ShoppingCartItem(
            qty=5,
            sku="sss",
            description="test",
            unit_price=Decimal("200.00"),
            discount=Decimal("0.2"),
        )

        self.assertEqual(Decimal("800.00"), sci.total)


class ShoppingCartTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.products = create_fake_products_storage()
        self.promocodes = [
            PromoCode("promo100", Decimal("100"), Decimal("200"))
        ]

    def test_add_item(self):

        sc = ShoppingCart("es", self.products, self.promocodes)

        product = self.products.get_product("PRODA")

        sc.add_item("PRODA", 2)

        self.assertIn("PRODA", sc._items)
        self.assertEqual(sc._items["PRODA"].product_sku, product.sku)
        self.assertEqual(sc._items["PRODA"].product_description, product.description)
        self.assertEqual(
            sc._items["PRODA"].product_unit_price, product.regions["es"].price
        )

        # TODO validate discount

    def test_get_total_with_items_with_no_discount(self):

        sc = ShoppingCart("ec", self.products, self.promocodes)

        sc.add_item("PRODA", 4)
        sc.add_item("PRODB", 2)

        self.assertEqual(Decimal("1140.00"), sc.get_total())
        self.assertTrue(sc.apply_promocode('promo100'))        
        # self.assertEqual(Decimal("2890.00"), sc.get_total())

    def test_get_total_with_items_with_discount(self):

        sc = ShoppingCart("es", self.products, self.promocodes)

        sc.add_item("PRODA", 4)
        sc.add_item("PRODB", 2)

        self.assertEqual(Decimal("945.00"), sc.get_total())
        self.assertTrue(sc.apply_promocode('promo100'))
        # self.assertEqual(Decimal("2355.00"), sc.get_total())

    def test_not_existing_promocode(self):
        sc = ShoppingCart("es", self.products, self.promocodes)

        sc.add_item("PRODA", 2)

        with self.assertRaises(Exception) as ctx:
            sc.apply_promocode("invalid")

        self.assertTrue("Promo code not found" in str(ctx.exception))

    

        

