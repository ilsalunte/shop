import decimal
from decimal import Decimal
from enum import Enum
from typing import NamedTuple
from basket import Basket
from user import UserWithoutPassword, HistoryItem
from warehouse import Warehouse
from users_handling import UsersHandling, WrongCredential


class Action(Enum):
    EXIT = 'wyjdź'
    LIST_PRODUCTS = 'wyświetl wszystkie dostępne produkty'
    FIND_PRODUCT = 'wyszukaj produkt'
    ADD_PRODUCT_TO_WAREHOUSE = 'dodaj produkt do magazynu'
    ADD_PRODUCT_TO_BASKET = 'dodaj produkt do koszyka'
    DELETE_PRODUCT_FROM_WAREHOUSE = 'usuń towar z magazynu'
    DELETE_PRODUCT_FROM_BASKET = 'usuń towar z koszyka'
    CHANGE_AMOUNT_IN_WAREHOUSE = 'zmień ilość towarów w magazynie'
    CHANGE_AMOUNT_IN_BASKET = 'zmień ilość towarów w koszyku'
    CHANGE_PRICE = 'zmień cenę towaru'
    CHANGE_USER_PASSWORD = 'zmiana hasło użytkownika'
    ADD_USER = 'dodaj użytkownika'
    DELETE_USER = 'usuń użytkownika'
    SHOW_USER = 'wyświetl dane użytkownika'
    FINALIZE = 'sfinalizuj zamówienie'
    LOGOUT = 'wyloguj się'


ADMIN_ACTIONS = (
    Action.EXIT,
    Action.LIST_PRODUCTS,
    Action.FIND_PRODUCT,
    Action.ADD_PRODUCT_TO_WAREHOUSE,
    Action.DELETE_PRODUCT_FROM_WAREHOUSE,
    Action.CHANGE_AMOUNT_IN_WAREHOUSE,
    Action.CHANGE_PRICE,
    Action.CHANGE_USER_PASSWORD,
    Action.ADD_USER,
    Action.DELETE_USER,
    Action.SHOW_USER,
    Action.LOGOUT
)


USER_ACTIONS = (
    Action.EXIT,
    Action.LIST_PRODUCTS,
    Action.FIND_PRODUCT,
    Action.ADD_PRODUCT_TO_BASKET,
    Action.DELETE_PRODUCT_FROM_BASKET,
    Action.CHANGE_AMOUNT_IN_BASKET,
    Action.FINALIZE,
    Action.LOGOUT
)


class WrongUserInput(Exception):
    pass


class NewProduct(NamedTuple):
    name: str
    price: Decimal
    amount: int


def login(users_handling: UsersHandling) -> UserWithoutPassword:

    while True:
        print('Zaloguj się do sklepu.')
        email = input('Podaj adres email:')
        password = input('Podaj hasło:')
        try:
            users_handling.login(email, password)
            users_handling.get_user(email)
            break
        except WrongCredential as ex:
            print(f'Wystąpił błąd: {ex}')
            continue
    return users_handling.get_user(email=email)


def choose_action(is_admin: bool) -> Action:
    print('Jaką akcję chcesz wykonać?')
    possible_actions = ADMIN_ACTIONS if is_admin else USER_ACTIONS
    options = {str(i): a for i, a in enumerate(possible_actions)}
    menu = '\n'.join(f'{i} - {a.value}' for i, a in options.items())
    selection = input(menu)
    try:
        action = options[selection]
    except KeyError:
        raise WrongUserInput('Wybrano nieprawidłową akcję.') from None

    return action


def define_product() -> tuple[str, Decimal, int]:
    print('Podaj nazwę produktu.')
    name = input()

    print('Podaj cenę produktu.')
    try:
        price = Decimal(input())
    except decimal.InvalidOperation:
        raise WrongUserInput('Podano nieprawidłową wartość.') from None

    print('Podaj ilość produktu.')
    try:
        amount = int(input())
    except ValueError:
        raise WrongUserInput('Podano nieprawidłową wartość.') from None

    return NewProduct(name=name, price=price, amount=amount)


def get_product_id() -> str:
    print('Podaj ID produktu.')
    product_id = input()
    return product_id


def list_products(warehouse: Warehouse) -> None:
    get_all_products = warehouse.get_products_list()
    print('\n'.join(f'{product.product_id}: {product.name}' for product in get_all_products))


def find_product(warehouse: Warehouse) -> None:
    print('Podaj ID produktu.')
    product_id = input()
    product = warehouse.get_single_product(product_id)
    print(f'{product.product_id} : {product.name}, '
          f'cena: {product.price}zł, ilość: {product.amount} sztuk')


def add_product_to_warehouse(warehouse: Warehouse) -> None:
    choice = define_product()
    warehouse.add_product(name=choice.name, price=choice.price, amount=choice.amount)


def delete_product_from_warehouse(warehouse: Warehouse) -> None:
    product_id = get_product_id()
    warehouse.delete_product(product_id=product_id)


def change_amount_in_warehouse(warehouse: Warehouse) -> None:
    product_id = get_product_id()
    print('Podaj nową ilość produktu.')
    new_amount = int(input())
    warehouse.change_product_amount(product_id=product_id, new_amount=new_amount)


def change_price(warehouse: Warehouse) -> None:
    product_id = get_product_id()
    print('Podaj nową cenę produktu.')
    new_price = Decimal(input())
    warehouse.change_product_price(product_id=product_id, new_price=new_price)


def change_user_password(user_handling: UsersHandling) -> None:
    print('Podaj nazwę użytkownika.')
    email = input()
    print('Podaj nowe hasło.')
    new_password = input()
    user_handling.change_password(email=email, new_password=new_password)


def add_user(user_handling: UsersHandling) -> None:
    print('Podaj email użytkownika.')
    email = input()
    print('Podaj hasło dodanego użytkownika.')
    password = input()
    print('Czy nowoutworzony użytkownik ma uprawnienia administratora? T/N')
    is_admin = input()
    if is_admin == 'T':
        user_handling.add_user(email=email, password=password, is_admin=True)
    elif is_admin == 'N':
        user_handling.add_user(email=email, password=password)


def delete_user(user_handling: UsersHandling) -> None:
    print('Podaj adres email użytkownika, który ma zostać usunięty.')
    email = input()
    user_handling.delete_user(email=email)


def show_user(user_handling: UsersHandling) -> None:
    print('Podaj email użytkownika.')
    email = input()
    user = user_handling.get_user(email=email)
    if user.history:
        history = user.history
    else:
        history = 'brak historii do wyświetlenia'

    print(f'{user.email}: {history}, {user.is_admin}')


def add_product_to_basket(basket: Basket) -> None:
    print('Podaj ID produktu.')
    product_id = input()
    print('Podaj ilość danego produktu.')
    amount = int(input())
    basket.add_product(product_id=product_id, amount=amount)


def delete_product_from_basket(basket: Basket) -> None:
    print('Podaj ID produktu.')
    product_id = input()
    basket.delete_product(product_id=product_id)


def change_amount_in_basket(basket: Basket) -> None:
    print('Podaj ID produktu, którego ilość w koszyku chcesz zmienić.')
    product_id = input()
    print('Podaj nową ilośc produktu.')
    new_amount = int(input())
    basket.change_product_amount(product_id=product_id, new_amount=new_amount)


def finalize(basket: Basket, warehouse: Warehouse, user_handling: UsersHandling, user: UserWithoutPassword) -> None:
    shopping = basket.finalize()
    for product_id, amount in shopping.items():
        product = warehouse.get_single_product(product_id=product_id)
        new_amount = product.amount - shopping[product_id]
        warehouse.change_product_amount(product_id=product_id, new_amount=new_amount)
        user_handling.add_to_history(
            email=user.email,
            item=HistoryItem(product_id, product.name, amount)
        )
    basket.clear()


def do_action(action: Action, warehouse: Warehouse, user_handling: UsersHandling, basket: Basket, user: UserWithoutPassword) -> None:

    match action:
        case Action.LIST_PRODUCTS:
            list_products(warehouse=warehouse)
        case Action.FIND_PRODUCT:
            find_product(warehouse=warehouse)
        case Action.ADD_PRODUCT_TO_WAREHOUSE:
            add_product_to_warehouse(warehouse=warehouse)
        case Action.DELETE_PRODUCT_FROM_WAREHOUSE:
            delete_product_from_warehouse(warehouse=warehouse)
        case Action.CHANGE_AMOUNT_IN_WAREHOUSE:
            change_amount_in_warehouse(warehouse=warehouse)
        case Action.CHANGE_PRICE:
            change_price(warehouse=warehouse)
        case Action.CHANGE_USER_PASSWORD:
            change_user_password(user_handling=user_handling)
        case Action.ADD_USER:
            add_user(user_handling=user_handling)
        case Action.DELETE_USER:
            delete_user(user_handling=user_handling)
        case Action.SHOW_USER:
            show_user(user_handling=user_handling)
        case Action.ADD_PRODUCT_TO_BASKET:
            add_product_to_basket(basket=basket)
        case Action.DELETE_PRODUCT_FROM_BASKET:
            delete_product_from_basket(basket=basket)
        case Action.CHANGE_AMOUNT_IN_BASKET:
            change_amount_in_basket(basket=basket)
        case Action.FINALIZE:
            finalize(basket=basket, warehouse=warehouse, user_handling=user_handling, user=user)


def main() -> None:
    warehouse = Warehouse()
    user_handling = UsersHandling()
    while True:
        basket = Basket()
        try:
            user = login(users_handling=user_handling)
        except (WrongCredential, WrongUserInput) as ex:
            print(f'Wystąpł błąd: {ex}')
        while True:
            try:
                action = choose_action(is_admin=user.is_admin)
                if action is Action.EXIT:
                    print('Dziękujemy za odwiedzenie naszego sklepu.')
                    break
                if action is Action.LOGOUT:
                    break
                do_action(action=action, warehouse=warehouse, user_handling=user_handling, basket=basket, user=user)
            except WrongUserInput as ex:
                print(f'Wystąpił błąd: {ex}')


if __name__ == '__main__':
    main()
