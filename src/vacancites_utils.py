class Vacancy:
    __slots__ = ['title', 'url', 'salary', 'description']

    def __init__(self, title: str, url: str, salary: str, description: str):
        self.title = title
        self.url = url
        self.salary = self._validate_salary(salary)
        self.description = description

    @staticmethod
    def _validate_salary(salary: str) -> str:
        """Validates the salary data."""
        if not salary or salary.lower() in ['не указана', '']:
            return 'Зарплата не указана'
        return salary

    def to_dict(self):
        """Convert the Vacancy object to a dictionary."""
        return {
            'title': self.title,
            'url': self.url,
            'salary': self.salary,
            'description': self.description
        }

    def __lt__(self, other):
        return self._salary_value() < other._salary_value()

    def __le__(self, other):
        return self._salary_value() <= other._salary_value()

    def __eq__(self, other):
        return self._salary_value() == other._salary_value()

    def __ne__(self, other):
        return self._salary_value() != other._salary_value()

    def __gt__(self, other):
        return self._salary_value() > other._salary_value()

    def __ge__(self, other):
        return self._salary_value() >= other._salary_value()

    def _salary_value(self) -> int:
        if 'не указана' in self.salary.lower():
            return 0
        salary_parts = self.salary.replace(" ", "").split('-')
        try:
            return int(salary_parts[0])
        except (ValueError, IndexError):
            return 0

    def __hash__(self):
        return hash((self.title, self.url, self.salary, self.description))

    def __repr__(self):
        return f"Vacancy({self.title!r}, {self.url!r}, {self.salary!r}, {self.description!r})"

    @classmethod
    def cast_to_object_list(cls, hh_vacancies):
        pass
