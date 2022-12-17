import decimal
from getpass import getpass
from decimal import Decimal
from enum import Enum
from typing import NamedTuple
from basket import Basket
from user import UserWithoutPassword, HistoryItem
from warehouse import Warehouse, ProductIdNotFound
from users_handling import UsersHandling, WrongCredential, UserIdNotFound


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
    CHANGE_USER_PASSWORD = 'zmień hasło użytkownika'
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
        print('Zaloguj się do sklepu.\n')
        email = input('Podaj adres email:')
        password = getpass('Podaj hasło:')  # getpass()nie działa w PyCharmie
        try:
            users_handling.login(email, password)
            print('\n')
            break
        except WrongCredential as ex:
            print(f'Wystąpił błąd: {ex}')
            continue
    return users_handling.get_user(email=email)


def choose_action(is_admin: bool) -> Action:
    print('Jaką akcję chcesz wykonać?\n')
    possible_actions = ADMIN_ACTIONS if is_admin else USER_ACTIONS
    options = {str(i): a for i, a in enumerate(possible_actions)}
    menu = '\n'.join(f'{i} - {a.value}' for i, a in options.items())
    selection = input(menu + '\n\n')
    try:
        action = options[selection]
    except KeyError:
        raise WrongUserInput('Wybrano nieprawidłową akcję.') from None

    return action


def define_product(warehouse: Warehouse) -> tuple[str, Decimal, int]:
    name = input('Podaj nazwę produktu.\n')
    if not warehouse.check_product_existence_name(name):
        print('Podaj cenę produktu')
        try:
            price = Decimal(input().replace(',', '.'))
        except decimal.InvalidOperation:
            raise WrongUserInput('Podano nieprawidłową wartość.') from None

        if price <= 0:
            raise WrongUserInput('Cena musi być większa od 0.')
        print('Podaj ilość produktu.')
        try:
            amount = int(input())
        except ValueError:
            raise WrongUserInput('Podano nieprawidłową wartość.') from None
        if amount <= 0:
            raise WrongUserInput('Ilość musi być większa od 0.')

        return NewProduct(name=name, price=price, amount=amount)

    raise WrongUserInput('Podany produkt już istnieje w magazynie.')


def get_product_id(warehouse: Warehouse) -> str:
    print('Podaj ID produktu.')
    product_id = input()
    if warehouse.check_product_existence(product_id):
        return product_id
    raise ProductIdNotFound('Nie znaleziono produktu o podanym ID.')


def list_products(warehouse: Warehouse) -> None:
    get_all_products = warehouse.get_products_list()
    print('\n' + '\n'.join(f'ID produktu {product.product_id}: {product.name}' for product in get_all_products))


def find_product(warehouse: Warehouse) -> None:
    product_id = get_product_id(warehouse=warehouse)
    product = warehouse.get_single_product(product_id)
    print(f'\n{product.product_id} : {product.name}, '
          f'cena: {product.price}zł, ilość: {product.amount} szt.')


def add_product_to_warehouse(warehouse: Warehouse) -> None:
    choice = define_product(warehouse)
    warehouse.add_product(name=choice.name, price=choice.price, amount=choice.amount)


def delete_product_from_warehouse(warehouse: Warehouse) -> None:
    product_id = get_product_id(warehouse=warehouse)
    warehouse.delete_product(product_id=product_id)


def change_amount_in_warehouse(warehouse: Warehouse) -> None:
    product_id = get_product_id(warehouse=warehouse)
    print('Podaj nową ilość produktu.')
    try:
        new_amount = int(input())
    except ValueError:
        raise WrongUserInput('Podano nieprawidłową wartość.') from None
    else:
        if new_amount <= 0:
            raise WrongUserInput('Ilość musi być więsza od 0.')
        warehouse.change_product_amount(product_id=product_id, new_amount=new_amount)


def change_price(warehouse: Warehouse) -> None:
    product_id = get_product_id(warehouse=warehouse)
    print('Podaj nową cenę produktu.')
    try:
        new_price = Decimal(input().replace(',', '.'))
    except decimal.InvalidOperation:
        raise WrongUserInput('Podano nieprawidłową wartość.') from None
    else:
        if new_price <= 0:
            raise WrongUserInput('Cena musi być więsza od 0.')
        warehouse.change_product_price(product_id=product_id, new_price=new_price)


def change_user_password(user_handling: UsersHandling) -> None:
    print('Podaj nazwę użytkownika.')
    email = input()
    if user_handling.check_user_existence(email=email):
        while True:
            print('Podaj nowe hasło.')
            new_password_first = input()
            print('Powtórz hasło.')
            new_password = input()
            if new_password_first == new_password:
                user_handling.change_password(email=email, new_password=new_password)
                break
            print('Podane hasła różnią się.')
    else:
        raise UserIdNotFound('Nie znaleziono podanego użytkownika.')


def add_user(user_handling: UsersHandling) -> None:
    while True:
        print('Podaj email użytkownika.')
        email = input()
        if user_handling.check_user_existence(email=email):
            print('Użytkownik o podanym adresie email już istnieje.')
            continue
        print('Podaj hasło dodanego użytkownika.')
        password_first = input()
        print('Powtórz hasło.')
        password = input()
        if password_first != password:
            print('Podan hasłą różnią się.')
            continue
        print('Czy nowoutworzony użytkownik ma uprawnienia administratora? T/N')
        is_admin = input().upper()
        if is_admin not in ('T', 'N'):
            print('Wybrano niedostępną opcję.')
            continue
        user_handling.add_user(email=email, password=password, is_admin=is_admin == 'T')
        break


def delete_user(user_handling: UsersHandling) -> None:
    print('Podaj adres email użytkownika, który ma zostać usunięty.')
    email = input()
    user_handling.delete_user(email=email)


def show_user(user_handling: UsersHandling) -> None:
    print('Podaj email użytkownika.')
    email = input()
    user = user_handling.get_user(email=email)

    if user.history:
        print(f'Login użytkownika: {user.email}\nCzy jest adminem: {user.is_admin}')
        history_str = '\n'.join(f'ID produktu: {item.product_id} Nazwa produktu: {item.product_name} '
                                f'Ilość zakupionego produktu: {item.amount}' for item in user.history)
        print(f'Historia zamówień: \n{history_str}')
    else:
        print(
            f'Login użytkownika: {user.email} \nCzy jest adminem: {"tak" if user.is_admin else "nie"}\n'
            f'Historia zamówień: brak historii do wyświetlenia'
        )


def add_product_to_basket(basket: Basket, warehouse: Warehouse) -> None:
    product_id = get_product_id(warehouse=warehouse)
    if basket.check_product_existence(product_id=product_id):
        raise WrongUserInput('Podany produkt już znajduje się w koszyku.')
    print('Podaj ilość danego produktu.')
    try:
        amount = int(input())
    except ValueError:
        raise WrongUserInput('Podano nieprawidłową wartość') from None
    warehouse_amount = warehouse.get_amount(product_id=product_id)
    if warehouse_amount < amount:
        raise WrongUserInput('Podana ilość przekracza ilosć produktów w magazynie.')
    if amount <= 0:
        raise WrongUserInput('Ilość dodanych produktów powinna być większa od 0.')
    basket.add_product(product_id=product_id, amount=amount)
    print('Produkt został dodany do koszyka.')


def delete_product_from_basket(basket: Basket, warehouse: Warehouse) -> None:
    product_id = get_product_id(warehouse=warehouse)
    try:
        basket.delete_product(product_id=product_id)
    except KeyError:
        raise WrongUserInput('W koszyku nie znaleziono podanego produktu.') from None
    else:
        print('Produkt został usunięty z koszyka.')


def change_amount_in_basket(basket: Basket, warehouse: Warehouse) -> None:
    print('Podaj ID produktu, którego ilość w koszyku chcesz zmienić.')
    product_id = input()
    if not basket.check_product_existence(product_id=product_id):
        raise ProductIdNotFound('W koszyku nie ma produktu o podanym ID.')
    print('Podaj nową ilośc produktu.')
    try:
        new_amount = int(input())
    except ValueError:
        raise WrongUserInput('Podano nieprawidłową wartość.') from None
    warehouse_amount = warehouse.get_amount(product_id=product_id)
    if new_amount <= 0:
        raise WrongUserInput('Ilość musi być większa od 0.')
    if warehouse_amount < new_amount:
        raise WrongUserInput('Podana ilość przekracza ilosć produktów w magazynie.')
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


def do_action(
        action: Action, warehouse: Warehouse, user_handling: UsersHandling, basket: Basket, user: UserWithoutPassword
) -> None:

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
            add_product_to_basket(basket=basket, warehouse=warehouse)
        case Action.DELETE_PRODUCT_FROM_BASKET:
            delete_product_from_basket(basket=basket, warehouse=warehouse)
        case Action.CHANGE_AMOUNT_IN_BASKET:
            change_amount_in_basket(basket=basket, warehouse=warehouse)

        case Action.FINALIZE:
            finalize(basket=basket, warehouse=warehouse, user_handling=user_handling, user=user)


def main() -> None:
    warehouse = Warehouse()
    user_handling = UsersHandling()
    while True:
        basket = Basket()
        try:
            user = login(users_handling=user_handling)
        except WrongCredential as ex:
            print(f'Wystąpł błąd: {ex}')
        while True:
            try:
                action = choose_action(is_admin=user.is_admin)
                if action is Action.EXIT:
                    print('Dziękujemy za odwiedzenie naszego sklepu.')
                    return
                if action is Action.LOGOUT:
                    break
                do_action(action=action, warehouse=warehouse, user_handling=user_handling, basket=basket, user=user)
                print('\n')
            except (WrongUserInput, ProductIdNotFound, UserIdNotFound) as ex:
                print(f'Wystąpił błąd: {ex}')


if __name__ == '__main__':
    main()
