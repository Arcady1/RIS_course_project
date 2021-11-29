# Сторонние пакеты
from flask import session, current_app


def get_session_group_name(user_type=None):
    """
    Функция инициализирует пользователя

    Args:
        user_type: str. Тип пользователя из файла config/access.json
    Returns:
        str. Тип пользователя, который зашел в систему
    """

    # Если group не указан, функция возвращает тип текущего пользователя
    if user_type is None:
        type_user = session.get('group_name', 'unauthorized')
        session['group_name'] = type_user

    # Иначе - переданного пользователя
    else:
        type_user = user_type
    show_name = current_app.config['ACCESS_CONFIG'][f"{type_user}"]["name"]
    return show_name
