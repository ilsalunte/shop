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
        self.add_product(name='pieprz', prize=Decimal('1.3'), amount=35)
        self.add_product(name='papryka ostra', prize=Decimal('1.5'), amount=40)

    def add_product(self, name: str, prize: Decimal, amount: int = 0) -> str:
        product_id = str(self._counter).zfill(3)

        product = Product(
            product_id=product_id,
            name=name,
            prize=prize,
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

    def change_product_prize(self, product_id: str, new_prize: Decimal) -> None:
        try:
            self._products[product_id].prize = new_prize
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
    test.add_product(name='czarnuszka', prize=Decimal('5.0'), amount=15)
    print(test.get_products_list())
    # test.delete_product(product_id='001')
    # added_2 = test.add_product(name='oregano', prize=Decimal('3.0'), amount=32)
    # test.change_product_prize(product_id='002', new_prize=Decimal('66.0'))
    # getting = test.get_products_list()
    # print('\n'.join(f'{hhh.product_id}: {hhh.name}' for hhh in getting))
    #
    # print(f'{ProductName.product_id}: {ProductName.name}')
    # getting_single = test.get_single_product('002')
    # print('moja')
    # print(getting_single)
    # print(f'{getting_single.product_id} : {getting_single.name}, '
    #       f'{getting_single.prize}zł, {getting_single.amount} sztuk')

    pass



