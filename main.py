from src.api import HeadHunterAPI
from src.vacancites_utils import Vacancy
from src.file_utils import JSONSaver

def filter_vacancies(vacancies, filter_words):
    """Filter vacancies based on keywords in the title or description."""
    return [
        vacancy for vacancy in vacancies
        if any(word.lower() in (vacancy.title or '').lower() or word.lower() in (vacancy.description or '').lower()
               for word in filter_words)
    ]

def get_vacancies_by_salary(vacancies, salary_range):
    """Filter vacancies within a given salary range."""
    min_salary, max_salary = map(int, salary_range.split('-'))
    return [
        vacancy for vacancy in vacancies
        if vacancy._salary_value() >= min_salary and vacancy._salary_value() <= max_salary
    ]


def sort_vacancies(vacancies):
    """Sort vacancies by salary in descending order."""
    return sorted(vacancies, key=lambda v: v._salary_value(), reverse=True)


def get_top_vacancies(vacancies, top_n):
    """Get the top N vacancies."""
    return vacancies[:top_n]


def print_vacancies(vacancies):
    """Print the list of vacancies."""
    for vacancy in vacancies:
        print(f"{vacancy.title}: {vacancy.salary} ({vacancy.url})")

def user_interaction():
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()

    search_query = input("Введите поисковый запрос: ")
    hh_vacancies = hh_api.get_vacancies(search_query)

    vacancies_list = [Vacancy(
        title=vacancy.get('name', 'Не указано'),
        url=vacancy.get('alternate_url', 'Не указано'),
        salary=_format_salary(vacancy.get('salary')),
        description=vacancy.get('snippet', {}).get('requirement', 'Нет описания')
    ) for vacancy in hh_vacancies]

    # Сохранение вакансий в JSON-файл
    for vacancy in vacancies_list:
        json_saver.add_vacancy(vacancy)
    print("Вакансии сохранены в файл.")

    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат (например: 100000-150000): ")

    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    print_vacancies(top_vacancies)

    # Добавление опции для удаления вакансий
    delete_url = input("Введите URL вакансии для удаления (или оставьте пустым, чтобы пропустить): ")
    if delete_url:
        for vacancy in vacancies_list:
            if vacancy.url == delete_url:
                json_saver.delete_vacancy(vacancy)
                print(f"Вакансия {vacancy.title} удалена.")
                break
        else:
            print("Вакансия с таким URL не найдена.")

# Helper function to format salary data
def _format_salary(salary_data):
    if not salary_data:
        return 'Не указана'
    salary_from = salary_data.get('from')
    salary_to = salary_data.get('to')
    currency = salary_data.get('currency', 'RUR')
    salary_str = f"{salary_from or ''}-{salary_to or ''} {currency}".strip('-')
    return salary_str

if __name__ == "__main__":
    user_interaction()