class Basket:
    def __init__(self):
        self._chosen_products: dict[str, int] = {}
        self.add_product('001', 2)
        self.add_product('000', 1)

    def add_product(self, product_id: str, amount: int) -> None:
        self._chosen_products[product_id] = self._chosen_products.get(product_id, 0) + amount

    def delete_product(self, product_id: str) -> None:
        del self._chosen_products[product_id]

    def change_product_amount(self, product_id: str, new_amount: int) -> None:
        self._chosen_products[product_id] = new_amount

    def finalize(self) -> dict[str, int]:
        return self._chosen_products

    def clear(self) -> None:
        self._chosen_products.clear()


if __name__ == '__main__':
    test = Basket()
    lista = test.finalize
    print(lista)

pass