""" Модуль для проверки валидности данных в форме """

# Встроенные модули
import re


def is_form_valid(data, expected_data_type, positive_num=None):
    """
    Функция проверяет, соответсвует ли переменная указанному типу данных

    Args:
        data: any. Значение, которое проверяется на переданный тип данных
        expected_data_type: any. Нужный тип данных, с которым сравнивается аргумент data
    Returns:
        Boolean. True - data соответствует типу данных expected_data_type, False - нет
    """
    # Строки
    if expected_data_type == str:
        if re.match(r'[а-яА-Яa-zA-Z]', data) is not None:
            return True
        else:
            return False
    # Числа
    elif expected_data_type == int or expected_data_type == float:
        # Положительное число
        if positive_num == True:
            try:
                if expected_data_type(data) >= 0:
                    return True
                else:
                    return False
            except:
                return False
        # Отрицательное число
        elif positive_num == False:
            try:
                if expected_data_type(data) < 0:
                    return True
                else:
                    return False
            except:
                return False
        # Положительное или отрицательное - не указано
        else:
            try:
                expected_data_type(data)
                return True
            except:
                return False
    else:
        return isinstance(data, expected_data_type)
