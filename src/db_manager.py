import psycopg2


class DBManager:
    """Класс для получения данных из БД в Postgres"""
    def __init__(self, db_name: str, tb_employers: str, tb_vacancies: str, params) -> None:
        """
        Создание экземпляра класса DBManager.
        :param db_name: имя базы данных
        :param tb_employers: название таблицы с данными о работодателе
        :param tb_vacancies: название таблицы с данными о вакансиях
        """
        self.db_name = db_name
        self.tb_employers = tb_employers
        self.tb_vacancies = tb_vacancies
        self.params = params
        self.params.update({'dbname': self.db_name})

    def get_companies_and_vacancies_count(self) -> list:
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        :return: list
        """
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cur:
                    data = []
                    cur.execute(f"""SELECT company_name, vacancies 
                    FROM {self.tb_employers}""")

                    for company in cur:
                        data.append(company)

                    return data

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()
