from decimal import Decimal
from typing import Dict
from products_storage import ProductsStorage


class PromoCodeChecker:

    available_promocodes = {}

    def __init__(self, promocodes: Dict) -> None:
        self.available_promocodes = promocodes

    def get_promo_code(promo_code):
        raise NotImplementedError()


class ShoppingCartItem:
    qty: int = None
    product_sku: str = None
    product_unit_price: Decimal = None
    product_description: str
    product_volume_discount: Decimal
    product_discount: Decimal


class ShoppingCart:

    def __init__(
        self, region: str, products: ProductsStorage, promocodes: PromoCodeChecker
    ) -> None:
        pass

    def add_product(sku: str, qty: int):
        raise NotImplementedError()

    def get_total_price(self):
        raise NotImplementedError()
