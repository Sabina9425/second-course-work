import unittest

from main import filter_vacancies, get_vacancies_by_salary, sort_vacancies, get_top_vacancies
from src.api import HeadHunterAPI
from src.file_utils import JSONSaver
from src.vacancites_utils import Vacancy


class TestVacancy(unittest.TestCase):

    def test_vacancy_initialization(self):
        vacancy = Vacancy("Python Developer", "https://hh.ru/vacancy/123456", "100 000-150 000 руб.",
                          "Требуется опыт от 3 лет...")
        self.assertEqual(vacancy.title, "Python Developer")
        self.assertEqual(vacancy.url, "https://hh.ru/vacancy/123456")
        self.assertEqual(vacancy.salary, "100 000-150 000 руб.")
        self.assertEqual(vacancy.description, "Требуется опыт от 3 лет...")

    def test_vacancy_salary_validation(self):
        vacancy = Vacancy("Python Developer", "https://hh.ru/vacancy/123456", "", "Требуется опыт от 3 лет...")
        self.assertEqual(vacancy.salary, "Зарплата не указана")

    def test_vacancy_comparison(self):
        vacancy1 = Vacancy("Python Developer", "https://hh.ru/vacancy/123456", "100 000 руб.",
                           "Требуется опыт от 3 лет...")
        vacancy2 = Vacancy("Java Developer", "https://hh.ru/vacancy/654321", "150 000 руб.", "Опыт от 5 лет...")
        self.assertTrue(vacancy2 > vacancy1)


class TestHeadHunterAPI(unittest.TestCase):

    def test_get_vacancies(self):
        hh_api = HeadHunterAPI()
        vacancies = hh_api.get_vacancies("Python")
        self.assertIsInstance(vacancies, list)


class TestJSONSaver(unittest.TestCase):

    def setUp(self):
        self.json_saver = JSONSaver(filename='test_vacancies.json')
        self.vacancy = Vacancy("Python Developer", "https://hh.ru/vacancy/123456", "100 000 руб.",
                               "Требуется опыт от 3 лет...")

    def tearDown(self):
        import os
        if os.path.exists('test_vacancies.json'):
            os.remove('test_vacancies.json')

    def test_add_vacancy(self):
        self.json_saver.add_vacancy(self.vacancy)
        vacancies = self.json_saver.get_vacancies({"title": "Python Developer", "salary_range": "50000-200000"})
        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0].title, "Python Developer")

    def test_delete_vacancy(self):
        self.json_saver.add_vacancy(self.vacancy)
        self.json_saver.delete_vacancy(self.vacancy)
        vacancies = self.json_saver.get_vacancies({})
        self.assertEqual(len(vacancies), 0)


class TestHelperFunctions(unittest.TestCase):

    def test_filter_vacancies(self):
        vacancies = [
            Vacancy("Python Developer", "https://hh.ru/vacancy/123456", "100 000 руб.", "Опыт от 3 лет..."),
            Vacancy("Java Developer", "https://hh.ru/vacancy/654321", "150 000 руб.", "Опыт от 5 лет...")
        ]
        filtered_vacancies = filter_vacancies(vacancies, ["Python"])
        self.assertEqual(len(filtered_vacancies), 1)
        self.assertEqual(filtered_vacancies[0].title, "Python Developer")

    def test_get_vacancies_by_salary(self):
        vacancies = [
            Vacancy("Python Developer", "https://hh.ru/vacancy/123456", "100 000 руб.", "Опыт от 3 лет..."),
            Vacancy("Java Developer", "https://hh.ru/vacancy/654321", "150 000 руб.", "Опыт от 5 лет...")
        ]
        ranged_vacancies = get_vacancies_by_salary(vacancies, "90000-120000")
        self.assertEqual(len(ranged_vacancies), 1)
        self.assertEqual(ranged_vacancies[0].title, "Python Developer")

    def test_sort_vacancies(self):
        vacancies = [
            Vacancy("Python Developer", "https://hh.ru/vacancy/123456", "100 000 руб.", "Опыт от 3 лет..."),
            Vacancy("Java Developer", "https://hh.ru/vacancy/654321", "150 000 руб.", "Опыт от 5 лет...")
        ]
        sorted_vacancies = sort_vacancies(vacancies)
        self.assertEqual(sorted_vacancies[0].title, "Java Developer")

    def test_get_top_vacancies(self):
        vacancies = [
            Vacancy("Python Developer", "https://hh.ru/vacancy/123456", "100 000 руб.", "Опыт от 3 лет..."),
            Vacancy("Java Developer", "https://hh.ru/vacancy/654321", "150 000 руб.", "Опыт от 5 лет...")
        ]
        top_vacancies = get_top_vacancies(vacancies, 1)
        self.assertEqual(len(top_vacancies), 1)
        self.assertEqual(top_vacancies[0].title, "Python Developer")
