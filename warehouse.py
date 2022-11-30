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
        try:
            del self._products[product_id]
        except KeyError:
            raise ProductIdNotFound from None

    def change_product_price(self, product_id: str, new_price: Decimal) -> None:
        try:
            self._products[product_id].price = new_price
        except KeyError:
            raise ProductIdNotFound from None

    def change_product_amount(self, product_id: str, new_amount: int) -> None:
        try:
            self._products[product_id].amount = new_amount
        except KeyError:
            raise ProductIdNotFound from None

    def get_single_product(self, product_id: str) -> Product:
        try:
            return self._products[product_id]
        except KeyError:
            raise ProductIdNotFound from None

    def get_products_list(self) -> list[ProductName]:
        return [
            ProductName(product_id=item.product_id, name=item.name)
            for item in self._products.values()
        ]


if __name__ == '__main__':
    test = Warehouse()
    test.add_product(name='czarnuszka', price=Decimal('5.0'), amount=15)
    print(test.get_products_list())
    # test.delete_product(product_id='001')
    # added_2 = test.add_product(name='oregano', price=Decimal('3.0'), amount=32)
    # test.change_product_price(product_id='002', new_price=Decimal('66.0'))
    # getting = test.get_products_list()
    # print('\n'.join(f'{hhh.product_id}: {hhh.name}' for hhh in getting))
    #
    # print(f'{ProductName.product_id}: {ProductName.name}')
    # getting_single = test.get_single_product('002')
    # print('moja')
    # print(getting_single)
    # print(f'{getting_single.product_id} : {getting_single.name}, '
    #       f'{getting_single.price}zł, {getting_sing
    #       le.amount} sztuk')

    pass



