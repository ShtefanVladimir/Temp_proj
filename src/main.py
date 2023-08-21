from src.connector import Connector
from src.engine_classes import HH, Superjob
from src.utils import sorting, get_top, get_hh_vacancies_list, get_sj_vacancies_list


def main():
    keyword = input("Введите ключевое слово для поиска вакансий: ")

    hh_engine = HH(keyword)
    sj_engine = Superjob(keyword)

    path = "hh_vacancies.json"

    hh_connector = Connector(path)
    hh_connector.clear()

    sj_connector = Connector("sj_vacancies.json")
    sj_connector.clear()

    page = 0
    hh_pages = 1
    hh_close = False
    more = True
    while not hh_close and more:
        if page < hh_pages:
            hh_engine.params["page"] = page
            page += 1
            hh_vacancies = hh_engine.get_request().json()
            hh_pages = hh_vacancies["pages"]
            hh_items = hh_vacancies["items"]
            hh_connector.insert(hh_items)
        else:
            hh_close = True

        if more:
            sj_engine.params["page"] = sj_engine.params["page"] + 1
            sj_vacancies = sj_engine.get_request().json()
            sj_items = sj_vacancies["objects"]
            more = sj_vacancies["more"]
            sj_connector.insert(sj_items)

    while True:
        command = input("Введите команду (sort или top): ")
        if command == "sort":
            hh_vacancies = get_hh_vacancies_list(hh_connector)
            sj_vacancies = get_sj_vacancies_list(sj_connector)
            sorted_vacancies = sorting(hh_vacancies + sj_vacancies)
            for vacancy in sorted_vacancies:
                print(vacancy)

        elif command == "top":
            hh_vacancies = get_hh_vacancies_list(hh_connector)
            sj_vacancies = get_sj_vacancies_list(sj_connector)
            all_vacancies = hh_vacancies + sj_vacancies
            top_count = int(input("Введите количество вакансий для вывода: "))
            top_vacancies = get_top(all_vacancies, top_count)
            for vacancy in top_vacancies:
                print(vacancy)

        else:
            print("Некорректная команда. Попробуйте ещё раз.")
        continue_running = input("Хотите продолжить работу с программой? (yes/no): ")
        if continue_running.lower() == "no":
            return


if __name__ == "__main__":
    main()
