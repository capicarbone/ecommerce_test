from decimal import Decimal
from typing import Dict
from products_storage import ProductsStorage


class PromoCodeChecker:

    def __init__(self, promocodes: Dict[str, str]) -> None:
        self.available_promocodes = {k.upper(): v for k, v in promocodes.items()}

    def check_promo_code(self, promo_code: str) -> Decimal:
        return Decimal(self.available_promocodes.get(promo_code, "0"))


class ShoppingCartItem:

    def __init__(
        self,
        qty: int,
        sku: str,
        description: str,
        unit_price: Decimal,
        discount=Decimal("0"),
        volume_discount: Decimal = None,
    ) -> None:
        self.qty = qty
        self.product_sku = sku
        self.product_description = description
        self.product_unit_price = unit_price
        self.discount_multiplier = Decimal("1") - discount
        self.product_volume_discount = volume_discount

    @property
    def total(self):
        return self.qty * self.product_unit_price * self.discount_multiplier


class ShoppingCart:

    def __init__(
        self, region: str, products: ProductsStorage, promocodes: PromoCodeChecker
    ) -> None:
        self.region_code = region
        self.products = products
        self.promo_codes = promocodes
        self._items: Dict[str, ShoppingCartItem] = {}

    def total_items(self) -> int:
        return len(self._items)

    def add_item(self, sku: str, qty: int):
        product = self.products.get_product(sku)

        sci = ShoppingCartItem(
            qty=qty,
            sku=product.sku,
            description=product.description,
            unit_price=product.regions[self.region_code].price,
            discount=product.regions[self.region_code].discount or Decimal("0"),
        )

        self._items[sku] = sci

    def get_total(self, promo_code: str = None):

        promo_discount = self.promo_codes.check_promo_code(promo_code) if promo_code else Decimal("0")

        total = sum([item.total for item in self._items.values()]) * (Decimal(1) - promo_discount)

        return total
