from api.hh_api import HeadHunterAPI
from api.sj_api import SuperJobAPI
from vacancy import Vacancy
from utils import save_to_json, hh_keywords_to_list


def stop_or_return():
    new_user_choice = input(f'По выбранным критериям вакансий не нашлось,'
                            f'попробуйте повторить снова, нажав "Enter" или введите "exit" для выхода\n')
    if new_user_choice == "exit":
        print('Всего доброго и до новых встреч!\n')
        exit()
    else:
        user_interaction()


def save_result_and_print(vacancy_objects_list):
    for vacancy in vacancy_objects_list:
        print(vacancy)
    save_to_json('data\\vacancies.csv', vacancy_objects_list)
    print(f'\nВакансии в количестве {len(vacancy_objects_list)} шт успешно загружены в файл vacancies.json')


def user_interaction():
    print('Добро пожаловать в программу поиска вакансий. ')
    user_platform = None
    while user_platform not in ('1', '2', '3'):
        user_platform = input('Введите цифру для выбора платформы: ('
                              'HeadHunter (hh.ru) - 1, '
                              'SuperJob (superjob.ru) - 2, '
                              'Обе платформы - 3)\n').strip()
        if user_platform not in ('1', '2', '3'):
            print('Проверьте правильность ввода и повторите снова')
    id_platform = int(user_platform) - 1
    print(f'Ваш выбор - {["HeadHunter", "SuperJob", "HeadHunter + SuperJob"][id_platform]}')

    sj_api = SuperJobAPI()
    hh_api = HeadHunterAPI()
    keywords = input(f'Введите ключевое слово для поиска вакансии, '
                    f'или ключевые слова, разделенные запятой: ').lower().strip()
    hh_keywords_list = hh_keywords_to_list(keywords)
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

    hh_api.add_keyword(keywords)
    sj_api.add_keyword(hh_keywords_list)
    sj_api.add_city(city)
    hh_api.add_city(city)

    vacancies = [hh_api.get_vacancies(),
                 sj_api.get_vacancies(),
                 hh_api.get_vacancies() + sj_api.get_vacancies()
                 ][id_platform]

    if not vacancies:
        stop_or_return()
    else:
        vacancy_objects = []
        for vacancy in vacancies:
            vacancy_objects.append(Vacancy(vacancy))
        amount = len(vacancy_objects)
        print(f'\nВакансии в количестве {amount} шт успешно загружены\n\n'
              f'Выберите, какое действие хотите выполнить далее. ')
        next_action = None
        while next_action not in ('1', '2', '3', '4', '5', '6'):
            next_action = input(f'Введите цифру для выбора: \n'
                                f'Вывести все вакансии без сортировки - 1 \n'
                                f'Вывести вакансии с сортировкой по возрастанию зарплаты - 2 \n'
                                f'Вывести вакансии с сортировкой по убыванию зарплаты - 3 \n'
                                f'Вывести топ-N вакансий по зарплате - 4 \n'
                                f'Вернуться в начало программы - 5 \n'
                                f'Выйти из программы - 6 \n').strip()
            if next_action not in ('1', '2', '3', '4', '5', '6'):
                print('Проверьте правильность ввода и повторите снова')
        match next_action:
            case '1':
                print('Список полученных вакансий без сортировки: \n')
                save_result_and_print(vacancy_objects)
            case '2':
                print('Список вакансий с сортировкой по возрастанию зарплаты: \n')
                vacancy_objects.sort(key=lambda vacancy_object: vacancy_object.salary_to)
                save_result_and_print(vacancy_objects)
            case '3':
                print('Список вакансий с сортировкой по убыванию зарплаты: \n')
                vacancy_objects.sort(key=lambda vacancy_object: vacancy_object.salary_to, reverse=True)
                save_result_and_print(vacancy_objects)

            case '4':
                vacancies_amount = ''
                while not vacancies_amount.isdigit():
                    vacancies_amount = input(f'Введите количество вакансий N, которое хотите получить. '
                                             f'Число должно быть не менее 1 и не более {amount} шт: ').strip()
                    if int(vacancies_amount) not in range(1, amount + 1):
                        print('Проверьте правильность ввода и повторите снова')
                vacancy_objects.sort(key=lambda vacancy_object: vacancy_object.salary_to)
                save_result_and_print(vacancy_objects[:int(vacancies_amount)])
            case '5':
                user_interaction()
            case '6':
                print('Всего доброго и до новых встреч!\n')
                exit()
