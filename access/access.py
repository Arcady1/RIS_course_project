# Сторонние пакеты
from flask import session, request, current_app, render_template

# Стандартные пакеты
from functools import wraps

def group_permission_validation(config: dict, sess: session) -> bool:
    """
    Функция проверяет, есть ли у пользователя доступ к endpoit-у

    Args:
        config: dict. Конфигурация пользователей с указанием доступных им endpoint-ов
        sess: session. Текущая сессия
    Returns:
        Boolean. True - есть доступ, False - нет доступа
    """
    group = sess.get('group_name')
    # Куда пользователь хочет обратиться. При len(splited_endpoint) = 0 - index.html
    splited_endpoint = request.path.replace('/', " ").strip().split(" ")
    target_app = "" if len(splited_endpoint) == 0 else splited_endpoint[-1]

    if (group in config.keys()) and (target_app in config[group]["url"]):
        return True
    return False

# Проверяет, есть ли пользователь в сессии
def login_permission_required(f):
    """
    Функция запускает проверку доступа пользователя к endpoint-у
    и возвращает либо запрошенную страницу, либо страницу "permission denied"

    Args:
        f: function. Функция, которая будет вызвана, если у пользователя есть доступ к endpoint-у
    Returns:
        wrapper: function.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if group_permission_validation(current_app.config['ACCESS_CONFIG'], session):
            return f(*args, **kwargs)
        return render_template('permission_denied.html')
    return wrapper