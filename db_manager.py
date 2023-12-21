import psycopg2

connect_string=("host='localhost' dbname='hh.ru' user='postgres' password='1234'")
connection = psycopg2.connect(connect_string)
cursor=connection.cursor()


class DBManager:

    @staticmethod
    def create_employer_table():
        sql = 'CREATE TABLE IF NOT EXISTS employer (id bigint, name varchar, descrip varchar);'
        cursor.execute(sql)
        connection.commit()

    @staticmethod
    def save_employer(employer):
        sql = 'INSERT INTO employer (id, name, descrip) VALUES (%s, %s, %s);'
        cursor.execute(sql,(employer['id'], employer['name'], employer['description']))
        connection.commit()

    @staticmethod
    def create_vacancy_table():
        sql = 'CREATE TABLE IF NOT EXISTS vacancy (id bigint, name varchar, alternate_url varchar, employer_id bigint, salary integer);'
        cursor.execute(sql)
        connection.commit()

    @staticmethod
    def save_vacancy(vacancy):
        sql = 'INSERT INTO vacancy (id, name, alternate_url, employer_id, salary) VALUES (%s, %s, %s, %s, %s);'
        cursor.execute(sql,(vacancy['id'], vacancy['name'], vacancy['alternate_url'], vacancy['employer_id'], vacancy['salary']))
        connection.commit()

    @staticmethod
    def get_companies_and_vacancies_count():
        """список всех компаний и количество вакансий у каждой компании."""
        print(DBManager.get_companies_and_vacancies_count.__doc__)
        sql = '''SELECT employer.id, count(vacancy.employer_id)
FROM employer
JOIN vacancy on employer.id = vacancy.employer_id
GROUP BY employer.id'''
        cursor.execute(sql)
        DBManager.outprint(cursor.fetchall())
        connection.commit()

    @staticmethod
    def get_all_vacancies():
        sql = '''SELECT employer.name, vacancy.name, vacancy.salary, vacancy.alternate_url
FROM vacancy
JOIN employer ON employer.id = vacancy.employer_id'''
        cursor.execute(sql)
        DBManager.outprint(cursor.fetchall())
        connection.commit()

    @staticmethod
    def get_avg_salary():
        sql = '''SELECT ROUND(AVG(salary), 2)
FROM vacancy
WHERE salary > 0'''
        cursor.execute(sql)
        DBManager.outprint(cursor.fetchall())
        connection.commit()

    @staticmethod
    def get_vacancies_with_higher_salary():
        sql = '''SELECT vacancy.name, salary
                    FROM vacancy
                    WHERE salary > (SELECT AVG(salary)
				    FROM vacancy
				    WHERE salary > 0)'''
        cursor.execute(sql)
        DBManager.outprint(cursor.fetchall())
        connection.commit()


    @staticmethod
    def get_vacancies_with_keyword(word: str):

        sql = f'''SELECT vacancy.name
FROM vacancy
WHERE LOWER(vacancy.name) LIKE ('%{word.lower()}%')'''
        cursor.execute(sql)
        DBManager.outprint(cursor.fetchall())
        connection.commit()


    @staticmethod
    def outprint(data):
        for line in data:
            print('=' * 100)
            print(*line, sep=' || ')

    @staticmethod
    def close_connection():
        connection.close()
