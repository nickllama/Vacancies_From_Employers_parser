import db_manager
import requests


class Request:

    employers = ['78638', '1740', '2624085', '15478', '816144', '3529', '3776', '3148', '2748', '733', '4181']
    url_vacancies = 'https://api.hh.ru/vacancies'
    url_employer = 'https://api.hh.ru/employers/{employer_id}'

    @staticmethod
    def create_tables():
        db_manager.DBManager.create_employer_table()
        db_manager.DBManager.create_vacancy_table()

    @staticmethod
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

    @classmethod
    def hh_parsing(cls):
        for employer in cls.employers:
            employer_info = requests.get(url=cls.url_employer.format(employer_id=employer))
            employer_info.encoding='utf-8'
            vacancies = requests.get(url=cls.url_vacancies,params={'employer_id':employer})
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
                    'salary': cls.get_salary(vacancy),
                }
                db_manager.DBManager.save_vacancy(vacancy_responce)