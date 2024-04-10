import requests


class HeadHunterAPI:
    """Класс для работы с API HeadHunter."""

    def __init__(self, employer_id: int):
        """
        Создание экземпляра класса HeadHunterAPI, где в employer_info будет храниться информация о работодателе,
        а в vacancies - вакансии работодателя.
        :param employer_id: id работодателя
        """
        if not isinstance(employer_id, int) or not employer_id:
            raise ValueError('Поисковый запрос должен быть непустой строкой.')

        self.employer_id = employer_id
        self.employer_info = {}
        self.vacancies = []

    def get_employer_info(self) -> None:
        """Получает информацию о работодателе."""

        url = f'https://api.hh.ru/employers/{self.employer_id}'
        try:
            response = requests.get(url)
            response.raise_for_status()  # Вызов исключения для кодов статуса 4xx/5xx
            data_json = response.json()
            self.employer_info = {'company_name': data_json['name'], 'url': data_json['site_url'],
                                  'vacancies': data_json['open_vacancies']}

        except requests.exceptions.RequestException as e:
            raise Exception(f'Ошибка при выполнении запроса: {e}.')

    def get_vacancies(self) -> None:
        """Получает информацию о вакансиях работодателя."""

        url = f'https://api.hh.ru/vacancies?employer_id={self.employer_id}'
        params = {'per_page': 100}

        try:
            page = 0
            while True:
                params['page'] = page
                response = requests.get(url, params=params)

                response.raise_for_status()  # Вызов исключения для кодов статуса 4xx/5xx

                data_json = response.json()

                if not data_json['items']:
                    break

                for vacancy_data in data_json['items']:
                    name = vacancy_data['name']

                    try:
                        salary_from = vacancy_data['salary']['from']
                    except TypeError:
                        salary_from = None

                    try:
                        salary_to = vacancy_data['salary']['to']
                    except TypeError:
                        salary_to = None

                    try:
                        salary_currency = vacancy_data['salary']['currency']
                    except TypeError:
                        salary_currency = 'Валюта не указана'

                    if salary_currency is None:
                        salary_currency = 'Валюта не указана'

                    city = vacancy_data['area']['name']
                    description = vacancy_data['snippet']['responsibility']
                    url_vacancy = vacancy_data['alternate_url']

                    vacancy = {
                        'name': name,
                        'salary_from': salary_from,
                        'salary_to': salary_to,
                        'salary_currency': salary_currency,
                        'city': city,
                        'description': description,
                        'url_vacancy': url_vacancy
                    }

                    self.vacancies.append(vacancy)
                page += 1

        except requests.exceptions.RequestException as e:
            raise Exception(f'Ошибка при выполнении запроса: {e}.')

    def __repr__(self):
        """Метод для отображения экземпляра класса HeadHunterAPI.
        :return: f-строка с данными.
        """
        result = f'employer_id={self.employer_id}, employer_info={self.employer_info}, vacancies={self.vacancies}'
        return f"HeadHunterAPI({result})"
