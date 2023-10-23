import copy
from abc import ABC, abstractmethod
import requests
from utils import remove_tags, convert_currency
from exceptions import ParsingError


class API(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def change_period(self):
        pass

    @abstractmethod
    def add_keyword(self, keywords):
        pass

    @abstractmethod
    def add_city(self):
        pass

    @abstractmethod
    def load_all_cities(self):
        pass


class HeadHunterAPI(API):

    HH_API_URL = 'https://api.hh.ru/vacancies'
    HH_API_URL_AREAS = 'https://api.hh.ru/areas'

    params_default = {
        'text': [],
        'area': 1,
        'per_page': 100,
        'date': 14
    }

    def __init__(self):
        self.params = copy.deepcopy(self.params_default)
        pass

    def change_period(self):
        pass

    def add_keyword(self, keywords):
        self.params['text'].append(keywords)

    def add_city(self):
        pass

    def load_all_cities(self):
        cities_params_list = requests.get(self.HH_API_URL_AREAS).json()
        return cities_params_list

    def get_vacancies(self):
        vc_list = []
        hh_ru_data = requests.get(self.HH_API_URL, self.params)
        code = hh_ru_data.status_code
        if code != 200:
            raise ParsingError(f'Ошибка получения вакансий! Статус-код: {code}')
        vacancies = hh_ru_data.json()['items']

        for vc in vacancies:
            if vc['salary'] is None:
                salary_from = 0
                salary_to = 0
                salary = 'Зарплата не указана'
            else:
                amount_from = int(vc['salary']['to']) if vc['salary']['to'] else 0
                salary_from = convert_currency(vc['salary']['currency'], amount_from)
                amount_to = int(vc['salary']['from']) if vc['salary']['from'] else 0
                salary_to = convert_currency(vc['salary']['currency'], amount_to)
                if salary_from:
                    if salary_to:
                        salary = f'Зарплата от {salary_from} до {salary_to}'
                    else:
                        salary = f'Зарплата от {salary_from}'
                else:
                    if salary_to:
                        salary = f'Зарплата до {salary_to}'
                    else:
                        salary = 'Зарплата не указана'

            # убираем html-теги из строки с требованиями
            if vc['snippet']['requirement']:
                reqs_without_text = remove_tags(vc['snippet']['requirement'])
            else:
                reqs_without_text = 'Требования не указаны'

            vc_list.append({
                'resource': 'HeadHunter',
                'id': vc['id'], 'name': vc['name'], 'city': vc['area']['name'], 'salary': salary,
                'url': vc['alternate_url'], 'work_mode': vc['employment']['name'],
                'salary_from': salary_from, 'salary_to': salary_to,
                'experience': vc['experience']['name'], 'employer': vc['employer']['name'],
                'employer_url': vc['employer'].get('alternate_url', 'Employer has not URL'), 'requirements': reqs_without_text[:170] + '...'
            })
        return vc_list
