from decimal import Decimal
from typing import Dict, List


class ProductRegion:
    region_code: str = None
    price: Decimal = None
    discount: Decimal = None

    def __init__(self, region_code: str, price: Decimal, discount: Decimal = None) -> None:
        self.region_code = region_code

        # TODO Validate
        self.price = price

        # TODO Validate
        self.discount = discount

    def __str__(self) -> str:
        pass


class Product:
    sku = None
    description = None
    regions = {}

    def __init__(self, sku: str, description: str) -> None:
        self.sku = sku
        self.description = description

    def add_region(self, region: ProductRegion) -> None:
        self.regions[region.region_code] = region

    def __str__(self) -> str:
        return f"({self.sku}) {self.description}"


class ProductsStorage:
    _available_regions: Dict
    _products : Dict[str, Product] = {}

    def __init__(self, available_regions: Dict) -> None:
        self._available_regions = {k.lower(): v for k, v in available_regions.items()}

    def is_valid_region(self, region_code: str):
        return region_code.lower() in self._available_regions.keys()

    def add_product(self, sku: str, description: str):
        self._products[sku] = Product(sku, description)

    def add_region_to_product(self, sku: str, region_code: str, price: Decimal, discount: Decimal = None):
        product = self._products[sku]

        product.add_region(ProductRegion(region_code, price, discount))

    def get_product(self, sku):
        return self._products[sku]