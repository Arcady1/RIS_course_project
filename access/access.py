from flask import session, request, current_app
from functools import wraps

# Функция проверяет, имеет ли текущий пользователь доступ к url, по которому он прошел
def group_permission_validation(config: dict, sess: session) -> bool:
    group = sess.get('group_name', 'unauthorized')
    sess['group_name'] = group
    # Куда пользователь хочет обратиться. При 1 - index.html
    target_app = "" if len(request.endpoint.split('.')) == 1 else request.endpoint.split('.')[0]

    if (group in config.keys()) and (target_app in config[group]['urls']):
        return True
    return False

def login_permission_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if group_permission_validation(current_app.config['ACCESS_CONFIG'], session):
            return f(*args, **kwargs)
        return 'Group permission denied'
    return wrapper