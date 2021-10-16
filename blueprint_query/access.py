from flask import session, request
from functools import wraps

# Есть ли у пользователя доступ
def group_validation(sess: session) -> bool:
    group = sess.get('group_name', None)
    if (group is not None) and (group != ''):
        return True
    else:
        return False

# Проверка существования пользователя и url в access.json
def group_permission_validation(config: dict, sess: session) -> bool:
    group = sess.get('group_name', 'unauthorized')
    # Куда пользователь хочет обратиться. При 1 - index
    target_app = "" if len(request.endpoint.split('.')) == 1 else request.endpoint.split('.')[0]
    if (group in config) and (target_app in config[group]):
        return True
    return False

# Декоратор для обработки доступа пользователя
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if group_validation(session):
            return f(*args, **kwargs)
        return 'Permission denied'
    return wrapper

def login_permission_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if group_permission_validation(current_app.config['ACCESS_CONFIG'], session):
            return f(*args, **kwargs)
        return 'Group permission denied'
    return wrapper