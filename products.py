from decimal import Decimal


class Product:
    def __init__(self, product_id: str, name: str, price: Decimal, amount: int = 0):
        self.product_id = product_id
        self.name = name
        self.amount = amount
        self.price = price

    def __repr__(self) -> str:
        return f'<{self.product_id}:{self.name}:{self.amount}:{self.price}>'
