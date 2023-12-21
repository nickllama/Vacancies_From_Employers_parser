import db_manager

choice_request = {
    1: db_manager.DBManager.get_companies_and_vacancies_count,
    2: db_manager.DBManager.get_all_vacancies,
    3: db_manager.DBManager.get_avg_salary,
    4: db_manager.DBManager.get_vacancies_with_higher_salary,
    5: db_manager.DBManager.get_vacancies_with_keyword
}