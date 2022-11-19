class Basket:
    def __init__(self):
        self._chosen_products: dict[str, int] = {}

    def add_product(self, product_id: str, amount: int) -> None:
        self._chosen_products[product_id] = amount

    #def summarize_shopping(self):


if __name__ == '__main__':
    test = Basket()
    print(test.add_product('001', 3))

pass