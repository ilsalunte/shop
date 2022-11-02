from shop.warehouse import Warehouse
from user import User
USERS = {'admin@admin': User(1, 'admin@admin', 'adminadmin', [], True)}


def main() -> None:
    warehouse = Warehouse()
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

    while True:
        if not USERS[email].is_admin:
            print('Jaką akcję chcesz wykonać?')
            action = input('1 - wyświetl wszystkie dostępne produkty\n'
                  '2 - wyszukaj produkt\n'
                  '3 - dodaj produkt do koszyka\n'
                  '4 - usuń towar z koszyka\n'
                  '5 - zmień ilość towarów w koszyku\n'
                  '6 - sfinalizuj zamówienie\n'
                  '7 - zmiana hasła'
                    '8 - wyjdź')

        else:
            print('Jaką akcję chcesz wykonać?')
            action = input('1 - wyświetl wszystkie dostępne produkty\n'
                  '2 - wyszukaj produkt\n'
                  '3 - dodaj produkt do magazynu\n'
                  '4 - usuń towar z magazynu\n'
                  '5 - zmień ilość towarów w magazynie\n'
                  '6 - zmień cenę towaru\n'
                  '7 - zmiana hasła użytkowników\n'
                  '8 - dodaj użytkownika\n'
                  '9 - usuń użytkownika\n'
                  '10 - wyświetl dane użytkownika\n'
                '11 - wyjdź')

        if action == '1':
            pass
        elif action == '2':
            pass
        elif action == '3':
            if USERS[email].admin == 'N':
                pass
            elif USERS[email].admin == 'Y':
                pass
        elif action == '4':
            if USERS[email].admin == 'N':
                pass
            elif USERS[email].admin == 'Y':
                pass
        elif action == '5':
            if USERS[email].admin == 'N':
                pass
            elif USERS[email].admin == 'Y':
                pass
        elif action == '6':
            if USERS[email].admin == 'N':
                pass
            elif USERS[email].admin == 'Y':
                pass
        elif action == '7':
            if USERS[email].admin == 'N':
                pass
            elif USERS[email].admin == 'Y':
                pass
        elif action == '8':
            pass
        elif action == '9':
            pass
        elif action == '10':
            pass
        else:
            print('Wybrano nieprawidłowe działanie.')


if __name__ == '__main__':
    main()
