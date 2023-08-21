from src.jobs_classes import Vacancy, HHVacancy, SJVacancy


def sorting(vacancies: list[Vacancy]) -> list[Vacancy]:
    """ Должен сортировать любой список вакансий по ежемесячной оплате (gt, lt magic methods) """
    return sorted(vacancies)


def get_top(vacancies: list[Vacancy], top_count: int) -> list[Vacancy]:
    """ Должен возвращать {top_count} записей из вакансий по зарплате (iter, next magic methods) """
    return list(sorted(vacancies, reverse=True)[:top_count])


def get_hh_vacancies_list(connector) -> list[HHVacancy]:
    vacancies = [
        HHVacancy(
            title=vacancy["name"],
            link=vacancy["alternate_url"],
            description=vacancy["snippet"],
            salary=vacancy["salary"]["from"] if vacancy["salary"] else None)
        for vacancy in connector.select({})]
    return vacancies


def get_sj_vacancies_list(connector) -> list[SJVacancy]:
    vacancies = [
        SJVacancy(
            title=vacancy["profession"],
            link=vacancy["link"],
            description=vacancy["candidat"],
            salary=vacancy["payment_from"])
        for vacancy in connector.select({})]
    return vacancies
