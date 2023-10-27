class Vacancy:
    def __init__(self, vacancy_data):
        self.id = vacancy_data['id']
        self.resource = vacancy_data['resource']
        self.name = vacancy_data['name']
        self.city = vacancy_data['city']
        self.employer = vacancy_data['employer']
        self.employer_url = vacancy_data['employer_url']
        self.work_mode = vacancy_data['work_mode']
        self.experience = vacancy_data['experience']
        self.url = vacancy_data['url']
        self.salary = vacancy_data['salary']
        self.salary_from = vacancy_data['salary_from']
        self.salary_to = vacancy_data['salary_to']
        self.requirements = vacancy_data['requirements']
        self.avg_salary = round((self.salary_from + self.salary_to) // 2)

    def __str__(self):
        return (
            f'''Ресурс: {self.resource}
            Город: {self.city}
            Название вакансии: {self.name}
            Ссылка на вакансию: {self.url}
            Средняя зарплата: {self.avg_salary if self.avg_salary else self.salary}
            Работодатель: {self.employer}
            Сылка на работодателя: {self.employer_url}
            Требуемый опыт: {self.experience}
            Требования: {self.requirements}
            Занятость: {self.work_mode}'''
        )