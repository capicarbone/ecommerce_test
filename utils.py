
from products_storage import ProductsStorage

fake_products = [
    ('ps4', 'Playstation 4'),
    ('xbox', 'Xbox'),
]

def create_fake_products_storage():
    storage = ProductsStorage(
        available_regions={
            'es': 'espana',
            'ec': 'ecuador',
            'mx': 'mexico'
        }
    )

    for sku, description in fake_products:
        storage.add_product(sku, description)

    return storage


