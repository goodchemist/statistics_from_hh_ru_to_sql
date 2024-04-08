import psycopg2


class PostgresDB:
    """Класс для работы с БД в Postgres"""

    def __init__(self, db_name, params) -> None:
        """
        Создание экземпляра класса PostgresDB.
        :param db_name: имя базы данных
        """
        self.db_name = db_name
        self.params = params
        self.params.update({'dbname': self.db_name})

    def create_table_employer(self, table_name) -> None:
        """
        Создает таблицу для хранения информации о работодателях.
        :param table_name: название таблицы
        :return: None
        """
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
                        employer_id SERIAL PRIMARY KEY,
                        company_name VARCHAR(255) NOT NULL,
                        url TEXT NOT NULL,
                        vacancies INTEGER
                        )
                        """)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

    def create_table_vacancy(self, table_name: str, table_employers: str) -> None:
        """
        Создает таблицу для хранения информации о вакансиях.
        :param table_name: название таблицы
        :param table_employers: название таблицы с данными о работодателе
        :return: None
        """
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
                        vacancy_id SERIAL PRIMARY KEY,
                        employer_id INTEGER,
                        name VARCHAR(255) NOT NULL,
                        salary_from INTEGER,
                        salary_to INTEGER,
                        salary_currency VARCHAR(30) NOT NULL,
                        city VARCHAR(100),
                        description TEXT,
                        url TEXT,
                        FOREIGN KEY (employer_id) REFERENCES {table_employers}(employer_id)
                        )
                        """)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

    def insert_to_table(self, tb_employer: str, tb_vacancies: str, employer: dict, vacancies: list[dict]) -> None:
        """
        Добавляет данные о работодателе в таблицу.
        :param tb_employer: название таблицы с данными о работодателе
        :param tb_vacancies: название таблицы с данными о вакансиях
        :param employer: словарь с данными о работодателе
        :param vacancies: список с данными о вакансиях
        :return: None
        """
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        f"""
                            INSERT INTO {tb_employer} (company_name, url, vacancies)
                            VALUES (%s, %s, %s)
                            RETURNING employer_id
                            """,
                        (employer['company_name'], employer['url'], employer['vacancies'])
                    )

                    employer_id = cur.fetchone()[0]
                    print(employer_id)
                    for vacancy in vacancies:
                        cur.execute(
                            f"""
                                    INSERT INTO {tb_vacancies} (employer_id, name, salary_from, salary_to, 
                                    salary_currency, city, description, url)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                """,
                            (employer_id, vacancy['name'], vacancy['salary_from'], vacancy['salary_to'],
                             vacancy['salary_currency'], vacancy['city'], vacancy['description'],
                             vacancy['url_vacancy'])
                        )

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()
