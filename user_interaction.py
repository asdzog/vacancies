from api.hh_api import HeadHunterAPI
from api.sj_api import SuperJobAPI
from vacancy import Vacancy
from utils import save_to_csv, save_to_json


def user_interaction():
    print('Добро пожаловать в программу поиска вакансий. ')
    requested_keyword = input('Введите ключевое слово для поиска вакансии: ').lower().strip()

    sj_api = SuperJobAPI()

    sj_api.add_keyword(requested_keyword)
    hh_api = HeadHunterAPI()
    hh_api.add_keyword(requested_keyword)
    vacancies = sj_api.get_vacancies() + hh_api.get_vacancies()
    sj_cities = sj_api.load_all_cities()
    hh_cities = hh_api.load_all_cities()

    vacancy_objects = []

    for vacancy in vacancies:
        vacancy_objects.append(Vacancy(vacancy))

    if vacancy_objects:

        for vacancy in vacancy_objects:
            print(vacancy)

        save_to_json('data\\vacancies.json', vacancy_objects)
        save_to_csv('data\\vacancies.csv', vacancy_objects)

    else:
        print('По выбранным ключевым словам вакансий не нашлось')
