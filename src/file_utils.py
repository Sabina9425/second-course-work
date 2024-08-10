from abc import ABC, abstractmethod
import json

from src.vacancites_utils import Vacancy


# Abstract class for file operations
class VacancyFileManager(ABC):

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy):
        """Add a vacancy to the file."""
        pass

    @abstractmethod
    def get_vacancies(self, criteria: dict):
        """Get vacancies from the file based on criteria."""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy):
        """Delete a vacancy from the file."""
        pass


class JSONSaver(VacancyFileManager):

    def __init__(self, filename='data/vacancies.json'):
        self._filename = filename

    def add_vacancy(self, vacancy: Vacancy):
        """Add a vacancy to the JSON file."""
        try:
            data = self._load_file()
            vacancies = data.get('items', [])  # Assuming vacancies are stored under the 'items' key
            if not any(v['url'] == vacancy.url for v in vacancies):
                vacancies.append(vacancy.to_dict())
                data['items'] = vacancies
                self._save_file(data)
        except FileNotFoundError:
            self._save_file({'items': [vacancy.to_dict()]})

    def get_vacancies(self, criteria: dict):
        """Get vacancies from the JSON file based on criteria."""
        data = self._load_file()
        vacancies = Vacancy.cast_to_object_list(data.get('items', []))
        result = [
            vacancy for vacancy in vacancies
            if (str(criteria.get('title', '')).lower() in vacancy.title.lower()) and
               (self._in_salary_range(vacancy.salary_value(), criteria.get('salary_range')))
        ]
        return result

    def delete_vacancy(self, vacancy: Vacancy):
        """Delete a vacancy from the JSON file."""
        data = self._load_file()
        vacancies = data.get('items', [])
        vacancies = [v for v in vacancies if v['url'] != vacancy.url]
        data['items'] = vacancies
        self._save_file(data)

    def _load_file(self):
        """Load vacancies from JSON file."""
        with open(self._filename, 'r', encoding='utf-8') as file:
            return json.load(file)

    def _save_file(self, data):
        """Save vacancies to JSON file."""
        with open(self._filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def _in_salary_range(salary_value: int, salary_range: tuple):
        min_salary, max_salary = map(int, salary_range.split('-'))
        return min_salary <= salary_value <= max_salary
