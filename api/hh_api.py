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
    def change_period(self, days):
        pass

    @abstractmethod
    def add_keyword(self, keywords):
        pass

    @abstractmethod
    def add_city(self, city):
        pass

    @abstractmethod
    def load_all_cities(self):
        pass


class HeadHunterAPI(API):

    HH_API_URL = 'https://api.hh.ru/vacancies'
    HH_API_URL_CITIES = 'https://api.hh.ru/areas'

    params_default = {
        'text': [],  # ключевое слово или их список
        'area': 1,  # поиск осуществляется по вакансиям города 1 - Москва
        'per_page': 100,  # число вакансий на странице
        'date': 7  # период времени для поиска
    }

    def __init__(self):
        self.params = copy.deepcopy(self.params_default)

    def change_period(self, days):
        self.params['period'] = days

    def add_keyword(self, keywords):
        self.params['text'].append(keywords)

    def add_city(self, city):
        self.params['area'] = self.load_all_cities()[city]

    def load_all_cities(self):
        cities = {}
        cities_dict = requests.get(self.HH_API_URL_CITIES).json()
        for k in cities_dict:
            for i in range(len(k['areas'])):
                if len(k['areas'][i]['areas']) != 0:
                    for j in range(len(k['areas'][i]['areas'])):
                        cities[k['areas'][i]['areas'][j]['name'].title()] = k['areas'][i]['areas'][j]['id']
                else:
                    cities[k['areas'][i]['name'].title()] = k['areas'][i]['id']
        return cities

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
                amount_to = int(vc['salary']['to']) if vc['salary']['to'] else 0
                salary_to = convert_currency(vc['salary']['currency'], amount_to)
                amount_from = int(vc['salary']['from']) if vc['salary']['from'] else 0
                salary_from = convert_currency(vc['salary']['currency'], amount_from)
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
