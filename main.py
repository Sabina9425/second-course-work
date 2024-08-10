from src.api import HeadHunterAPI
from src.utils import filter_vacancies, get_vacancies_by_salary, sort_vacancies, get_top_vacancies, print_vacancies
from src.vacancites_utils import Vacancy
from src.file_utils import JSONSaver

def user_interaction():
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()

    search_query = input("Введите поисковый запрос: ")
    hh_vacancies = hh_api.get_vacancies(search_query)

    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)

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

if __name__ == "__main__":
    user_interaction()
