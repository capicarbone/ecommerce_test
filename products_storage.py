from decimal import Decimal
from typing import List


class ProductRegion:
    region: str = None
    price: Decimal = None
    discount: Decimal = None

    def __str__(self) -> str:
        pass


class Product:
    sku = None
    description = None
    regions = {}

    def __str__(self) -> str:
        return f"({self.sku}) {self.description}"


class ProductsStorage:
    available_regions: List[str] = {}
    products = {}

    def __init__(self, available_regions) -> None:
        self.available_regions = available_regions

    def add_product():
        raise NotImplementedError()

    def add_region_to_product(sku: str, region: str, price: Decimal, discount: Decimal):
        raise NotImplementedError()
