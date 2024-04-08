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
