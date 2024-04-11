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
        self._params = params
        self._params.update({'dbname': self.db_name})

    def get_companies_and_vacancies_count(self) -> list:
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        :return: list
        """
        try:
            with psycopg2.connect(**self._params) as conn:
                with conn.cursor() as cur:
                    data = []
                    cur.execute(f"""SELECT company_name, vacancies 
                    FROM {self.tb_employers}""")

                    return cur.fetchall()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

    def get_all_vacancies(self) -> list:
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию.
        :return: list
        """
        try:
            with psycopg2.connect(**self._params) as conn:
                with conn.cursor() as cur:

                    cur.execute(f"""SELECT name, {self.tb_vacancies}.url, {self.tb_employers}.company_name,
                    salary_to, salary_from, salary_currency
                    FROM {self.tb_vacancies}
                    JOIN {self.tb_employers} USING(employer_id)
                    
                    """)

                    return cur.fetchall()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

    def get_avg_salary(self, salary_currency: str) -> float:
        """Получает среднюю зарплату по вакансиям в зависимости от выбранной валюты зарплаты.
        :param salary_currency: валюта зарплаты
        :return: число
        """
        try:
            with psycopg2.connect(**self._params) as conn:
                with conn.cursor() as cur:

                    data = []
                    cur.execute(f"""SELECT salary_to, salary_from
                    FROM {self.tb_vacancies}
                    WHERE salary_currency =  '{salary_currency}'
                    """)

                    for company in cur:
                        data.append(company)

                    average_salary = []
                    for item in data:
                        average = self.calculate_avg_salary(item[0], item[1])
                        if average != 0:
                            average_salary.append(average)

                    result = round(sum(average_salary) / len(average_salary), 2)

                    return result

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def calculate_avg_salary(salary_to, salary_from) -> int | float:
        """
        Метод для расчета среднего значения зарплаты из диапазона 'от'-'до', если они указаны.
        :param salary_to: зарплата 'от'
        :param salary_from: зарплата 'до'
        :return: среднее значение диапазона зарплаты или 0, если диапазоны не указаны
        """
        if salary_to is None:
            if salary_from is None:
                return 0
            elif isinstance(salary_from, (int, float)):
                return salary_from

        elif salary_from is None:
            if isinstance(salary_to, (int, float)):
                return salary_to

        else:
            return (salary_to + salary_from) / 2

    def get_vacancies_with_keyword(self, keyword: str) -> list:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод keyword.
        :param keyword: ключевое слово/слова для поиска
        :return: список вакансий
        """
        keyword = keyword.lower()

        try:
            with psycopg2.connect(**self._params) as conn:
                with conn.cursor() as cur:

                    cur.execute(f"""SELECT name, {self.tb_vacancies}.url, {self.tb_employers}.company_name,
                    salary_to, salary_from, salary_currency
                    FROM {self.tb_vacancies}
                    JOIN {self.tb_employers} USING(employer_id)
                    WHERE LOWER(name) LIKE '%{keyword}' 
                    OR LOWER(name) LIKE '%{keyword}%' 
                    OR LOWER(name) LIKE '{keyword}%'
                    """)

                    return cur.fetchall()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

    def __repr__(self):
        """Метод для отображения экземпляра класса DBManager.
        :return: f-строка с данными.
        """
        return f"DBManager(db_name={self.db_name}, tb_employers={self.tb_employers}, tb_vacancies={self.tb_vacancies})"
