from utils import choice_request
from hh_requests import Request
from db_manager import DBManager


def main():
    """ Выводит диалог"""
    Request.create_tables()
    Request.hh_parsing()
    while True:
        print()
        print('Выберите запрос: ')
        print("1 - список всех компаний и количество вакансий у каждой компании.\n"
              "2 - список всех вакансий с указанием названия компании,"
              " названия вакансии и зарплаты и ссылки на вакансию.\n"
              "3 - средняя зарплата по вакансиям.\n"
              "4 - список всех вакансий, у которых зарплата выше средней по всем вакансиям.\n"
              "5 - список всех вакансий, в названии которых содержатся ключевое слово, например python.\n"
              "0 - Завершение работы программы")

        a = int(input('Введите запрос: '))
        if a == 5:
            choice_request.get(a)((input('Введите слово для поиска поиска по базе  ')))
        elif 0 < a < 5:
            choice_request.get(a)()
        elif a == 0:
            DBManager.close_connection()
            print('До скорой встречи!')
            break
        else:
            print('такого запроса не существует')


if __name__ == "__main__":
    main()
