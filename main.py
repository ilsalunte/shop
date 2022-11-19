from decimal import Decimal
from typing import NamedTuple
from basket import Basket
from shop.user import User, UserWithoutPassword
from shop.users_handling import UsersHandling, WrongCredential
from warehouse import Warehouse

ACTIONS_ADMIN = '0 - wyjdź\n' \
                '1 - wyświetl wszystkie dostępne produkty\n' \
                '2 - wyszukaj produkt\n' \
                '3 - dodaj produkt do magazynu\n' \
                '4 - usuń towar z magazynu\n' \
                '5 - zmień ilość towarów w magazynie\n' \
                '6 - zmień cenę towaru\n' \
                '7 - zmiana hasła użytkowników\n' \
                '8 - dodaj użytkownika\n' \
                '9 - usuń użytkownika\n' \
                '10 - wyświetl dane użytkownika'

ACTIONS_USER = '0 - wyjdź' \
               '1 - wyświetl wszystkie dostępne produkty\n' \
               '2 - wyszukaj produkt\n' \
               '3 - dodaj produkt do koszyka\n' \
               '4 - usuń towar z koszyka\n' \
               '5 - zmień ilość towarów w koszyku\n' \
               '6 - sfinalizuj zamówienie\n' \
               '7 - zmiana hasła'


class NewProduct(NamedTuple):
    name: str
    prize: Decimal
    amount: int


def login(users_handling: UsersHandling) -> str:

    while True:
        print('Zaloguj się do sklepu.')
        email = input('Podaj adres email:')
        password = input('Podaj hasło:')
        try:
            users_handling.login(email, password)
            break
        except WrongCredential():
            print('Podano nieprawidłowe dane logowania.')
            continue
    return email


def choose_action(verification: UserWithoutPassword) -> str:

    print('Jaką akcję chcesz wykonać?')

    if not verification.is_admin:
        action = input(ACTIONS_USER)
        return action

    action = input(ACTIONS_ADMIN)
    return action


def define_product() -> tuple[str, Decimal, int]:
    print('Podaj nazwę produktu.')
    name = input()

    print('Podaj cenę produktu.')
    prize = Decimal(input())

    print('Podaj ilość produktu.')
    amount = int(input())

    return NewProduct(name=name, prize=prize, amount=amount)


def get_product_id() -> str:
    print('Podaj ID produktu.')
    product_id = input()
    return product_id


def do_actions(
        action: str, email: str, verification: UserWithoutPassword,
        warehouse_operation: Warehouse, user_handling: UsersHandling) -> None:

    if action == '1':
        get_all_products = warehouse_operation.get_products_list()
        print('\n'.join(f'{product.product_id}: {product.name}' for product in get_all_products))

    elif action == '2':
        print('Podaj ID produktu.')
        product_id = input()
        product = warehouse_operation.get_single_product(product_id)
        print(f'{product.product_id} : {product.name}, '
              f'cena: {product.prize}zł, ilość: {product.amount} sztuk')

    elif action == '3':
        if verification.is_admin:
            choice = define_product()
            warehouse_operation.add_product(name=choice.name, prize=choice.prize, amount=choice.amount)
        # else:
        #     print('Podaj ID produktu.')
        #     product_id = input()
        #     print('Podaj ilość danego produktu.')
        #     amount = input()
        #
        #     basket_operation.add_product(product_id=product_id, amount=amount)

    elif action == '4':
        if verification.is_admin:
            product_id = get_product_id()
            warehouse_operation.delete_product(product_id=product_id)

    elif action == '5':
        if verification.is_admin:
            product_id = get_product_id()
            print('Podaj nową ilość produktu.')
            new_amount = int(input())
            warehouse_operation.change_product_amount(product_id=product_id, new_amount=new_amount)

    elif action == '6':
        if verification.is_admin:
            product_id = get_product_id()
            print('Podaj nową cenę produktu.')
            new_prize = Decimal(input())
            warehouse_operation.change_product_prize(product_id=product_id, new_prize=new_prize)

    elif action == '7':
        if verification.is_admin:
            print('Podaj nazwę użytkownika.')
            email = input()
            print('Podaj nowe hasło.')
            new_password = input()
            user_handling.change_password(email=email, new_password=new_password)



def main() -> None:
    user_handling = UsersHandling()
    email = login(users_handling=user_handling)
    warehouse_operation = Warehouse()
    while True:
        user_verification = user_handling.get_single_user(email)
        action = choose_action(verification=user_verification)
        if action == '0':
            print('Dziękujemy za odwiedzenie naszego sklepu.')
            break
        do_actions(action=action, email=email, verification=user_verification,
                   warehouse_operation=warehouse_operation, user_handling=user_handling)




# elif action == '4':
#     if USERS[email].admin == 'N':
#         pass
#     elif USERS[email].admin == 'Y':
#         pass
# elif action == '5':
#     if USERS[email].admin == 'N':
#         pass
#     elif USERS[email].admin == 'Y':
#         pass
# elif action == '6':
#     if USERS[email].admin == 'N':
#         pass
#     elif USERS[email].admin == 'Y':
#         pass
# elif action == '7':
#     if USERS[email].admin == 'N':
#         pass
#     elif USERS[email].admin == 'Y':
#         pass
# elif action == '8':
#     pass
# elif action == '9':
#     pass
# elif action == '10':
#     pass
# else:
#     print('Wybrano nieprawidłowe działanie.')


if __name__ == '__main__':
    main()

