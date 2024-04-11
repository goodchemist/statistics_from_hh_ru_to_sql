from src.config import config
from src.headhunterapi import HeadHunterAPI
from src.postgres_db import PostgresDB
from src.db_manager import DBManager
from tabulate import tabulate


def main():
    # Список id работодателей с HH.ru
    company_list = [2657797, 5612066, 3060194, 2628254, 3571722, 3731347, 5744540, 8975022, 3832271, 5472891]

    # Создание списка с экземплярами класса HeadHunterAPI для каждого работодателя
    company_hh = [HeadHunterAPI(company) for company in company_list]

    # Получение информации о работодателе и вакансиях
    for company in company_hh:
        company.get_employer_info()
        company.get_vacancies()

    # Параметры для подключения к БД
    params = config()

    # Название БД и таблиц, где будет храниться информация о работодателях и вакансиях
    name_db = 'hh_ru'
    table_employer = 'employers'
    table_vacancy = 'vacancies'

    # Создание таблиц в БД
    postgres_db = PostgresDB(name_db, params)
    postgres_db.create_table_employer(table_employer)
    postgres_db.create_table_vacancy(table_vacancy, table_employer)

    # Добавление информации в таблицы
    for company in company_hh:
        postgres_db.insert_to_table(table_employer, table_vacancy, company.employer_info, company.vacancies)

    # Экземпляр класса DBManager для получения информации из БД
    db_manager = DBManager(name_db, table_employer, table_vacancy, params)

    while True:
        answer = input(
            "Выберите нужный вариант:\n1 - Получить список всех компаний и количество вакансий у каждой компании.\n"
            "2 - Получить список всех вакансий с указанием названия компании, названия вакансии, зарплаты"
            "и ссылки на вакансию.\n"
            "3 - Получить среднюю зарплату по вакансиям в зависимости от выбранной валюты зарплаты.\n"
            "4 - Получить все вакансии, в названии которых содержится нужная фраза/слово.\n"
            "5 - Завершить программу.\n"
        ).strip()
        if answer == '1':
            print('Список всех компаний и количество вакансий у каждой компании:\n')

            print(tabulate(db_manager.get_companies_and_vacancies_count(), headers=['Компания', 'Количество вакансий'],
                           colalign=("left", "right")) + '\n')
        elif answer == '2':
            print(tabulate(db_manager.get_all_vacancies(),
                           headers=['Название вакансии', 'Ссылка на вакансию', 'Компания', 'Зарплата ОТ', 'Зарплата ДО',
                                    'Валюта зарплаты'], colalign=("left", "right")) + '\n')

        elif answer == '3':
            salary_currency = input('Введите валюту (RUR - рубли, USD - доллары, KZT - тенге): ').strip().upper()
            print(f'Средняя зарплата по вакансия с оплатой в {salary_currency}: '
                  f'{db_manager.get_avg_salary(salary_currency)}.\n')

        elif answer == '4':
            keyword = input('Введите ключевое слово или фразу для поиска: ').strip().lower()
            print(f'Список всех вакансий с указанием "{keyword}":\n')
            print(tabulate(db_manager.get_vacancies_with_keyword(keyword),
                           headers=['Название вакансии', 'Ссылка на вакансию', 'Компания', 'Зарплата ОТ', 'Зарплата ДО',
                                    'Валюта зарплаты'], colalign=("left", "right")) + '\n')

        elif answer == '5':
            break

        else:
            print('Попробуйте еще раз.\n')


if __name__ == '__main__':
    main()
