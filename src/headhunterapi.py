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
