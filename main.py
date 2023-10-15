from api import HeadHunterAPI, SuperJobAPI

from pprint import pprint


if __name__ == '__main__':
    sj_api = SuperJobAPI()    # vacancies = hh_api.get_vacancies()
    cities = sj_api.load_all_cities()
    pprint(cities, indent=2)

