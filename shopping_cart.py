from decimal import Decimal
from typing import Dict, List
from products_storage import ProductsStorage


class PromoCode:
    def __init__(self, code: str, discount: Decimal, threshold: Decimal) -> None:
        self.code = code
        self.discount = discount
        self.threshold = threshold


class ShoppingCartItem:

    def __init__(
        self,
        qty: int,
        sku: str,
        description: str,
        unit_price: Decimal,
        discount=Decimal("0"),
        volume_discount = Decimal("0"),
        percentage_volume_discount = Decimal("0")

    ) -> None:
        self.qty = qty
        self.product_sku = sku
        self.product_description = description
        self.product_unit_price = unit_price
        self.discount_multiplier = Decimal("1") - discount
        self.volume_discount = volume_discount
        self.volume_discount_multiplier = Decimal("1") - percentage_volume_discount

    @property
    def total(self):
        #import pdb; pdb.set_trace()
        return (
            self.qty * self.product_unit_price * self.discount_multiplier * self.volume_discount_multiplier
        ) - self.volume_discount


class ShoppingCart:

    def __init__(
        self,
        region: str,
        products: ProductsStorage,
        available_promocodes: List[PromoCode],
    ) -> None:
        self.region_code = region
        self.products = products
        self.promocodes = {p.code.upper(): p for p in available_promocodes}
        self._items: Dict[str, ShoppingCartItem] = {}

        self.promocode_discount = Decimal("0")

    def total_items(self) -> int:
        return len(self._items)

    def add_item(self, sku: str, qty: int):
        product = self.products.get_product(sku)

        unit_price = product.regions[self.region_code].price
        volume_discount = Decimal("0")
        percentage_volume_discount = Decimal("0")

        for discount_by_volume in product.discounts_by_volume:
            if qty >= discount_by_volume.qty_threshold:                
                percentage_volume_discount = discount_by_volume.percentage_discount or percentage_volume_discount                
                volume_discount = discount_by_volume.amount_discount or volume_discount
                break

        sci = ShoppingCartItem(
            qty=qty,
            sku=product.sku,
            description=product.description,
            unit_price=unit_price,
            discount=product.regions[self.region_code].discount or Decimal("0"),
            volume_discount=volume_discount,
            percentage_volume_discount=percentage_volume_discount
        )

        self._items[sku] = sci

    @property
    def gross_total(self):
        return sum([item.total for item in self._items.values()])

    def apply_promocode(self, promo_code: str) -> bool:
        upper_promocode = promo_code.upper()

        if upper_promocode in self.promocodes:
            if self.gross_total > self.promocodes[upper_promocode].threshold:
                self.promocode_discount = self.promocodes[upper_promocode].discount
                return True
            else:
                return False
        else:
            raise Exception("Promo code not found.")

    def get_total(self):
        return self.gross_total - self.promocode_discount
