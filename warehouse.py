from decimal import Decimal
from typing import NamedTuple
from products import Product


class ProductIdNotFound(Exception):
    pass


class ProductName(NamedTuple):
    product_id: str
    name: str


class Warehouse:
    def __init__(self):
        self._products: dict[str, Product] = {}
        self._counter = 0
        self.add_product(name='siodło', price=Decimal('2500'), amount=12)
        self.add_product(name='czaprak czerwony', price=Decimal('65'), amount=40)
        self.add_product(name='ostrogi', price=Decimal(45), amount=37)

    def add_product(self, name: str, price: Decimal, amount: int = 0) -> str:
        product_id = str(self._counter).zfill(3)

        product = Product(
            product_id=product_id,
            name=name,
            price=price,
            amount=amount
        )

        self._products[product_id] = product

        self._counter += 1
        return product_id

    def delete_product(self, product_id: str) -> None:
        del self._products[product_id]

    def change_product_price(self, product_id: str, new_price: Decimal) -> None:
        self._products[product_id].price = new_price

    def change_product_amount(self, product_id: str, new_amount: int) -> None:
        self._products[product_id].amount = new_amount

    def get_single_product(self, product_id: str) -> Product:
        return self._products[product_id]

    def get_products_list(self) -> list[ProductName]:
        return [
            ProductName(product_id=item.product_id, name=item.name)
            for item in self._products.values()
        ]

    def check_product_existence(self, product_id: str) -> bool:
        return product_id in self._products

    def check_product_existence_name(self, name: str) -> bool:
        for product in self._products.values():
            if product.name == name:
                return True
        return False

    def get_amount(self, product_id: str) -> int:
        return self._products[product_id].amount


if __name__ == '__main__':
    pass
