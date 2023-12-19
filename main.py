import requests
import db_manager

employers = ['78638', '1740', '2624085', '15478', '816144', '3529', '3776', '3148', '2748', '733', '4181']


url_vacancies = 'https://api.hh.ru/vacancies'
url_employer = 'https://api.hh.ru/employers/{employer_id}'
db_manager.DBManager.create_employer_table()
db_manager.DBManager.create_vacancy_table()
db_manager.DBManager.get_companies_and_vacancies_count()
db_manager.DBManager.get_all_vacancies()
db_manager.DBManager.get_avg_salary()
db_manager.DBManager.get_vacancies_with_higher_salary()
db_manager.DBManager.get_vacancies_with_keyword(input('Введите слово для поиска   '))

def get_salary(vacancy):
    if vacancy['salary']:
        to = vacancy['salary']['to']
        from_ = vacancy['salary']['from']
        if to and from_:
            salary = (int(to) + int(from_))/2

        elif to:
            salary = to

        else:
            salary = from_

    else:
        salary = 0

    return salary


for employer in employers:
    employer_info = requests.get(url=url_employer.format(employer_id=employer))
    employer_info.encoding='utf-8'
    vacancies = requests.get(url=url_vacancies,params={'employer_id':employer})
    employer_responce = {
        'id':employer_info.json()['id'],
        'name': employer_info.json()['name'],
        'description': employer_info.json()['description']
    }
    db_manager.DBManager.save_employer(employer_responce)

    for vacancy in vacancies.json()['items']:
        vacancy_responce = {
            'id': vacancy['id'],
            'name': vacancy['name'],
            'alternate_url': vacancy['alternate_url'],
            'employer_id': employer,
            'salary': get_salary(vacancy),
        }
        db_manager.DBManager.save_vacancy(vacancy_responce)