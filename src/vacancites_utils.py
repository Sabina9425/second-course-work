class Vacancy:
    def __init__(self, name, link, salary, requirements):
        self.name = name
        self.link = link
        self.salary = salary
        self.requirements = requirements

    @classmethod
    def cast_to_object_list(cls, hh_vacancies):
        pass