from user import User
from decimal import Decimal
from shop.warehouse import Warehouse

USERS = {'admin@admin': User(1, 'admin@admin', 'adminadmin', [], True)}
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
               '7 - zmiana hasła' \



def log_in() -> str:
    while True:
        print('Zaloguj się do sklepu.')
        email = input('Podaj adres email:')
        password = input('Podaj hasło:')
        try:
            USERS[email]
        except KeyError:
            print('Podano nieprawidłowe dane logowania.')
            continue

        if not password == USERS[email].user_password:
            print('Podano nieprawidłowe dane logowania.')
            continue
        break
    return email


def choose_action(email: str) -> str:
    print('Jaką akcję chcesz wykonać?')

    if not USERS[email].admin:
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

    return name, prize, amount


def do_actions(action: str, email: str) -> None:
    operation = Warehouse()
    if action == '0':
        pass
    elif action == '1':
        get_all_products = operation.get_products_list()
        print('\n'.join(f'{product.product_id}: {product.name}' for product in get_all_products))
    elif action == '2':
        print('Podaj ID produktu.')
        product_id = input()
        get_one_product = operation.get_single_product(product_id)
        print(f'{get_one_product.product_id} : {get_one_product.name}, '
              f'{get_one_product.prize}zł, {get_one_product.amount} sztuk')
    elif action == '3':
        if USERS[email].admin:
            choice = define_product()
            operation.add_product(name=choice[0], prize=choice[1], amount=choice[2])
    # elif action == '4':
    #     if USERS[email].admin:


def main() -> None:
    email = log_in()
    while True:
        action = choose_action(email)
        do_actions(action, email)

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
