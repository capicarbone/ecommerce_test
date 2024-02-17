from decimal import Decimal
from typing import Dict, List

from validators import is_valid_amount, is_valid_percentage


class DiscountByVolume:

    def __init__(
        self, qty_threshold: int, percentage_discount: Decimal, amount_discount: Decimal
    ) -> None:

        if not percentage_discount and not amount_discount:
            raise Exception(
                "Either percentage_discount or amount_discount is required."
            )

        if qty_threshold < 1:
            raise Exception("Invalid threshold")

        if percentage_discount and not is_valid_percentage(percentage_discount):
            raise Exception("Invalid percentage.")

        if amount_discount and not is_valid_amount(amount_discount):
            raise Exception("Invalid amount")

        self.qty_threshold = qty_threshold
        self.percentage_discount = percentage_discount
        self.amount_discount = amount_discount


class ProductRegion:

    def __init__(
        self, region_code: str, price: Decimal, discount: Decimal = None
    ) -> None:
        self.region_code = region_code

        # TODO Validate
        self.price = price

        # TODO Validate
        self.discount = discount

    def __str__(self) -> str:
        pass


class Product:

    def __init__(self, sku: str, description: str) -> None:
        self.sku: str = sku
        self.description: str = description
        self.regions: Dict[str, ProductRegion] = {}
        self.discounts_by_volume: List[DiscountByVolume] = []

    def add_region(self, region: ProductRegion) -> None:
        self.regions[region.region_code] = region

    def add_discount_by_volume(self, discount: DiscountByVolume) -> None:
        self.discounts_by_volume.append(discount)
        self.discounts_by_volume.sort(key=lambda x: x.qty_threshold, reverse=True)

    def __str__(self) -> str:
        return f"({self.sku}) {self.description}"


class ProductsStorage:

    def __init__(self, available_regions: Dict) -> None:
        self._products: Dict[str, Product] = {}
        self._available_regions = {k.lower(): v for k, v in available_regions.items()}

    def is_valid_region(self, region_code: str):
        return region_code.lower() in self._available_regions.keys()

    def add_product(self, sku: str, description: str):
        self._products[sku] = Product(sku, description)

    def add_region_to_product(
        self, sku: str, region_code: str, price: Decimal, discount: Decimal = None
    ):
        product = self._products[sku]

        if not is_valid_amount(price):
            raise Exception(f"Invalid price: {price}")

        if discount and not is_valid_percentage(discount):
            raise Exception(f"Invalid discount: {discount}")

        product.add_region(ProductRegion(region_code, price, discount))

    def add_discount_by_volume_to_product(
        self,
        sku: str,
        threshold: int,
        amount_discount: Decimal = None,
        percentage_discount: Decimal = None,
    ):
        product = self._products[sku]
        product.add_discount_by_volume(
            DiscountByVolume(
                qty_threshold=threshold,
                percentage_discount=percentage_discount,
                amount_discount=amount_discount,
            )
        )

    def get_product(self, sku):
        return self._products[sku]
