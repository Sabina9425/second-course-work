class Vacancy:
    __slots__ = ['title', 'url', 'salary', 'description']

    def __init__(self, title: str, url: str, salary: str, description: str):
        self.title = title
        self.url = url
        self.salary = self._validate_salary(salary)
        self.description = description

    def _validate_salary(self, salary: str) -> str:
        """Validates the salary data."""
        if not salary or salary.lower() in ['не указана', '']:
            return 'Зарплата не указана'
        return salary

    def __lt__(self, other):
        """Compares two vacancies by salary."""
        return self._salary_value() < other._salary_value()

    def __le__(self, other):
        """Compares two vacancies by salary."""
        return self._salary_value() <= other._salary_value()

    def __eq__(self, other):
        """Compares two vacancies by salary."""
        return self._salary_value() == other._salary_value()

    def __ne__(self, other):
        """Compares two vacancies by salary."""
        return self._salary_value() != other._salary_value()

    def __gt__(self, other):
        """Compares two vacancies by salary."""
        return self._salary_value() > other._salary_value()

    def __ge__(self, other):
        """Compares two vacancies by salary."""
        return self._salary_value() >= other._salary_value()

    def _salary_value(self) -> int:
        """Extracts the salary value for comparison, handling ranges and missing data."""
        if 'не указана' in self.salary.lower():
            return 0
        # Assuming salary is given in a format like "100 000-150 000 руб."
        salary_parts = self.salary.replace(" ", "").split('-')
        try:
            return int(salary_parts[0])
        except (ValueError, IndexError):
            return 0  # Fallback in case of unexpected format

    def __repr__(self):
        return f"Vacancy({self.title!r}, {self.url!r}, {self.salary!r}, {self.description!r})"

    @classmethod
    def cast_to_object_list(cls, hh_vacancies):
        pass
