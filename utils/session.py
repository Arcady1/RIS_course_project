# Сторонние пакеты
from flask import session, current_app

def get_session_group_name():
    """
    Функция инициализирует пользователя

    Returns:
        str. Тип пользователя, который зашел в систему
    """
    user_type = session.get('group_name', 'unauthorized')
    session['group_name'] = user_type
    show_name = current_app.config['ACCESS_CONFIG'][f"{user_type}"]["name"]
    return show_name