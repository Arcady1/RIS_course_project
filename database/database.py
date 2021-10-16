import pymysql
import pymysql.err as OperationalError

class DBConnection:
    # конструктор инициализации объекта, принимает config (словарь)
    def __init__(self, config: dict):
        self.config = config
        self.cursor = None
        self.connection = None

    # установка соединения с базой данных
    def __enter__(self):
        try:
            self.connection = pymysql.connect(**self.config)
            self.cursor = self.connection.cursor()
            return self.cursor
        except OperationalError:
            return None

    # завершение соединения с базой данных (уборка)
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
    result = []

    with DBConnection(config) as cursor:
        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]
        for item in cursor.fetchall():
            result.append(dict(zip(schema, item)))
    return result