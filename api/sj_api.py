from abc import ABC, abstractmethod
import requests
import copy
from utils import remove_tags, convert_currency
import os
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


class SuperJobAPI(API):
    """
    Класс для работы с API superjob.ru
    """
    SJ_API_URL = 'https://api.superjob.ru/2.0/vacancies'
    SJ_API_URL_AREAS = 'https://api.superjob.ru/2.0/towns'
    # SJ_TOKEN = os.getenv('SJ_API_KEY')
    SJ_TOKEN = 'v3.r.137503922.05a7d0fbd6b9ca56087f1e69b1bd87d60a1a83c4.78f3fff96e0950f0e141fc24c16505625fce56a8'

    params_default = {
        'keyword': [],  # Текст фильтра. В имени должна быть профессия
        'town': 1,  # Поиск осуществляется по вакансиям города 1 - Москва
    }

    def __init__(self):
        self.params = copy.deepcopy(self.params_default)
        pass

    def get_vacancies(self):
        headers = {'X-Api-App-Id': self.SJ_TOKEN}
        sj_ru_data = requests.get(self.SJ_API_URL, headers=headers, params=self.params)

        code = sj_ru_data.status_code
        if code != 200:
            raise ParsingError(f'Ошибка получения вакансий! Статус-код: {code}')

        vacancies = sj_ru_data.json()['objects']

        vc_list = []
        for vc in vacancies:
            if vc['payment_from']:
                if vc['payment_to']:
                    salary = f'Зарплата от {vc["payment_from"]} до {vc["payment_to"]} {vc["currency"]}'
                else:
                    salary = f'Зарплата от {vc["payment_from"]} {vc["currency"]}'
            else:
                if vc['payment_to']:
                    salary = f'Зарплата до {vc["payment_to"]} {vc["currency"]}'
                else:
                    salary = 'Зарплата не указана'

            # убираем html-теги из строки с требованиями
            reqs_without_text = remove_tags(vc['vacancyRichText'])

            salary_from = convert_currency(vc["currency"], int(vc["payment_from"]))
            salary_to = convert_currency(vc["currency"], int(vc["payment_to"]))
            vc_list.append({
                'resource': 'SuperJob',
                'id': vc['id'], 'name': vc['profession'],
                'city': vc['town']['title'], 'salary': salary,
                'salary_from': salary_from, 'salary_to': salary_to,
                'url': vc['link'], 'work_mode': vc['type_of_work']['title'],
                'experience': vc['experience']['title'],
                'employer': vc['client'].get('title', "Работодатель не указан"),
                'employer_url': vc['client'].get('link', 'Employer has not URL'),
                'requirements': reqs_without_text[:170] + '...'
            })
        return vc_list

    def change_period(self):
        pass

    def add_keyword(self, keywords):
        self.params['keyword'].append(keywords)

    def add_city(self):
        pass

    def load_all_cities(self):
        cities_params_list = requests.get(self.SJ_API_URL_AREAS).json()
        return cities_params_list
