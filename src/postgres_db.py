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
