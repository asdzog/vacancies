import copy
from abc import ABC, abstractmethod
import requests
import os


class API(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def change_period(self, period):
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
        #'key_word': 'python',  # ключевые слова
        'text': ['python'],  # Текст фильтра. В имени должна быть профессия
        'area': 40,  # Поиск ощуществляется по вакансиям города 1 - Москва
        #'page': 1,  # индекс страницы поиска на HH
        'per_page': 100,  # кол-во вакансий на 1 странице
        'date': 14
    }

    def __init__(self):
        self.params = copy.deepcopy(self.params_default)
        pass

    def get_vacancies(self):
        hh_ru_data = requests.get(self.HH_API_URL, self.params).json()
        return hh_ru_data['items']

    def change_period(self, period):
        self.params['date'] = period

    def add_keyword(self, keywords):
        self.params['text'].extend(keywords)

    def add_city(self):
        pass

    def load_all_cities(self):
        return requests.get(self.HH_API_URL_AREAS).json()


class SuperJobAPI(API):

    SJ_API_URL = 'https://api.superjob.ru/2.0/vacancies'
    SJ_API_URL_AREAS = 'https://api.superjob.ru/2.0/towns'
    SJ_TOKEN = os.getenv('SJ_API_KEY')

    params_default = {
        # 'key_word': 'python',  # ключевые слова
        'keyword': ['python'],  # Текст фильтра. В имени должна быть профессия
        'town': 40,  # Поиск ощуществляется по вакансиям города 1 - Москва
        # 'page': 1,  # индекс страницы поиска на HH
        'count': 100,  # кол-во вакансий на 1 странице
        'period': 1
    }

    def __init__(self):
        self.params = copy.deepcopy(self.params_default)
        pass

    def get_vacancies(self):
        headers = {
            'X-Api-App-Id': self.SJ_TOKEN
        }
        sj_ru_data = requests.get(self.SJ_API_URL, headers=headers, params=self.params).json()
        return sj_ru_data

    def change_period(self, period):
        self.params['date'] = period

    def add_keyword(self, keywords):
        self.params['text'].extend(keywords)

    def add_city(self):
        pass

    def load_all_cities(self):
        return requests.get(self.SJ_API_URL_AREAS).json()


