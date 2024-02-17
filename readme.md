
# Prueba de carrito de compras

# Sobre la implementacion

Se ha implementado con Python 3.x, sin alguna dependencia fuera de la instacion de Python 3, por lo que no es necesario instalar algún modulo.

Para el diseño de la solución se ha seguido un enfoque de POO y como metodologia se ha seguido TDD.

Entre los tests se han implementado los diferentes ejemplos que se encuentran en el enunciado enviado. Estos tests corresponden a aquellos con los nombres `test_example_case_x`, en la clase `ShoppingCarTestCase` en el archivo `tests.py`.

## Ejecutar tests

Es posible ejecutar todos los tests con el comando

```bash
python -m unittest
```

Si se quiere correr algún test en especifico:

```bash
python3 -m unittest tests.ShoppingCartTestCase.test_example_case_1
```

## Uso

Se debe primero crear un storage de productos con las diferentes regionse que estarán disponibles.

```python

from products_storage import ProductsStorage

storage = ProductsStorage(
        available_regions={"es": "espana", "ec": "ecuador", "mx": "mexico"}
    )
```

Luego en este storage es posible agregar productos con sus precios y descuentos por regiones:

```python

from decimal import Decimal

storage.add_product(sku, description)
storage.add_region_to_product(
            sku,
            region_code,
            Decimal(price),
            Decimal(discount),
        )
```

También es posible agregar descuentos por volumen a los productos usando el storage:

```python

storage.add_discount_by_volume_to_product(
    sku,
    threshold=threshold,  # Cantidad minima para aplicar el descuento
    amount_discount=Decimal(amount_discount), # Descuento de valor fijo
    percentage_discount=None, # Descuento por porcentage
)
```

Por facilidad es posible usar una function en utils.py para crear un conjunto de productos basados en los ejemplo proporcionados en el enunciado:

```python
from utils import create_fake_products_storage

storage = create_fake_products_storage()
```

Luego es posible crear una lista de códigos promocionales:

```python
from shopping_cart import PromoCode

promocodes = [
    PromoCode("promo100", 
    Decimal("100"), # Descuento
    Decimal("200")) # Monto minimo para aplicar el codigo
]
```

Con estas configuraciones podemos entonces instanciar un objeto ShoppingCart

```python
from shopping_cart import ShoppingCart

sc = ShoppingCart("es", # Codigo de la region
    storage, 
    promocodes
)
```

Con el objeto de ShoppingCart podemos agregar productos usado el sku de cada producto:

```python

sc.add_item('PRODA', 4)
sc.add_item('PRODB', 110)
```

También podemos aplicar códigos de promocion

```python
sc.apply_promocode('promo100')
```

Por ultimo podemos pedir el total a pagar:

```python
sc.get_total()
```







