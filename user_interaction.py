from api.hh_api import HeadHunterAPI
from api.sj_api import SuperJobAPI
from vacancy import Vacancy
from utils import save_to_csv, save_to_json


def user_interaction():
    print('Добро пожаловать в программу поиска вакансий. ')
    sj_api = SuperJobAPI()
    hh_api = HeadHunterAPI()
    keyword = input('Введите ключевое слово для поиска вакансии: ').lower().strip()
    city = input('Введите город для поиска вакансии: ').title().strip()
    sj_cities = sj_api.load_all_cities()
    hh_cities = hh_api.load_all_cities()

    while not sj_cities.get(city) or not hh_cities.get(city):
        city = input(f'Ошибка в названии или город не найден, повторите ввод.\n'
                     f"Для выбора города по умолчанию введите 'default'\n").title().strip()
        if city.lower() == 'default':
            city = 'Москва'
            print('Выбран город Москва по умолчанию')
            break

    hh_api.add_keyword(keyword)
    sj_api.add_keyword(keyword)
    sj_api.add_city(city)
    hh_api.add_city(city)

    vacancies = hh_api.get_vacancies() + sj_api.get_vacancies()
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
