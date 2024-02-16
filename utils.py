from decimal import Decimal

from products_storage import ProductsStorage

fake_products = [
    (
        "PRODA",
        "Producto A",
        [("es", "50.00", "0.1"), ("ec", "60.00", None)],
        [
            (3, "45", None),       
        ],
    ),
    (
        "PRODB", "Product B", [("es", "1.5", None), ("ec", "2", None)], 
        [
            (10, "5", None),
            (50, None, "0.1"),
            (200, None, "0.2"),
        ]
    ),
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
