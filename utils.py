from decimal import Decimal

from products_storage import ProductsStorage

fake_products = [
    (
        "ps4",
        "Playstation 4",
        [("es", "500.00", "0.2"), ("ec", "500.00", None)],
        [
            (5, "200", None),
            (10, "500", None),
            (15, None, "0.2"),
        ],
    ),
    ("xbox", "Xbox", [("es", "450", "0.15"), ("ec", "450.00", None)], []),
]


def create_fake_products_storage():
    storage = ProductsStorage(
        available_regions={"es": "espana", "ec": "ecuador", "mx": "mexico"}
    )

    for sku, description, regions, discounts_by_volume in fake_products:
        storage.add_product(sku, description)

        for region in regions:
            region_code, price, discount = region
            storage.add_region_to_product(
                sku,
                region_code,
                Decimal(price),
                Decimal(discount) if discount else None,
            )

        for discount_by_volume in discounts_by_volume:
            threshold, amount_discount, percentage_discount = discount_by_volume
            storage.add_discount_by_volume_to_product(
                sku,
                threshold=threshold,
                amount_discount=Decimal(amount_discount) if amount_discount else None,
                percentage_discount=(
                    Decimal(percentage_discount) if percentage_discount else None
                ),
            )

    return storage
