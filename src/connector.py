import json
import os


class Connector:
    """
    Класс коннектор к файлу, обязательно файл должен быть в json формате
    не забывать проверять целостность данных, что файл с данными не подвергся
    внешнего деградации
    """

    def __init__(self, file_path):
        self.__data_file = file_path
        self.__connect()

    @property
    def data_file(self):
        return self.__data_file

    @data_file.setter
    def data_file(self, value):
        self.__data_file = value
        self.__connect()

    def __connect(self):
        """
        Проверка на существование файла с данными и
        создание его при необходимости
        Также проверить на деградацию и возбудить исключение
        если файл потерял актуальность в структуре данных
        """
        if not os.path.exists(self.__data_file):
            with open(self.__data_file, 'w') as file:
                file.write(json.dumps([]))

    def load_data(self):
        with open(self.__data_file, 'r') as file:
            return json.load(file)

    def clear(self):
        self.__connect()

    def insert(self, data: list[dict]):
        """
        Запись данных в файл с сохранением структуры и исходных данных
        """
        file_data = self.load_data()
        new_vacancies = []
        ids = [vac["id"] for vac in file_data]
        for vacancy in data:
            pk = vacancy["id"]
            if pk not in ids:
                new_vacancies.append(vacancy)
        with open(self.__data_file, 'w') as file:
            json.dump(file_data + new_vacancies, file, indent=4, ensure_ascii=False)

    def select(self, query: dict):
        """
        Выбор данных из файла с применением фильтрации
        query содержит словарь, в котором ключ это поле для
        фильтрации, а значение это искомое значение, например:
        {'price': 1000}, должно отфильтровать данные по полю price
        и вернуть все строки, в которых цена 1000
        """
        file_data = self.load_data()

        if not query:
            return file_data

        result = []
        for entry in file_data:
            if all(entry.get(key) == value for key, value in query.items()):
                result.append(entry)
        return result

    def delete(self, query):
        """
        Удаление записей из файла, которые соответствуют запрос,
        как в методе select. Если в query передан пустой словарь, то
        функция удаления не сработает
        """
        if not query:
            return
        file_data = self.load_data()
        result = []
        for entry in file_data:
            if not all(entry.get(key) == value for key, value in query.items()):
                result.append(entry)
        with open(self.__data_file, 'w') as file:
            json.dump(result, file)
