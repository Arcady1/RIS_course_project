# Сторонние пакеты
import pymysql
import pymysql.err as OperationalError

class DBConnection:
    """
    Класс инициализирует соединения с базой данных
    """

    # Конструктор инициализации объекта, принимает файл конфигурации
    def __init__(self, config: dict):
        self.config = config
        self.cursor = None
        self.connection = None

    # Установка соединения с базой данных
    def __enter__(self):
        try:
            self.connection = pymysql.connect(**self.config)
            self.cursor = self.connection.cursor()
            return self.cursor
        except OperationalError:
            return None

    # Завершение соединения с базой данных (уборка)
    def __exit__(self, exc_type, exc_val, exc_trace):
        if self.connection is not None and self.cursor is not None:
            self.connection.commit()
            self.connection.close()
            self.cursor.close()
        if exc_val is not None:
            print(exc_type)
            print(exc_val.args)
        return True


def work_with_db(config, sql):
    """
    Функция выполняет запрос к БД и возвращает результат

    Args:
        config: dict. Конфигурация для подключения к базе данных
        sql: str. SQL запрос
    Returns:
        result: list. Лист словарей - результаты запрососв
    """
    result = []

    with DBConnection(config) as cursor:
        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]

        for item in cursor.fetchall():
            result.append(dict(zip(schema, item)))
    return result