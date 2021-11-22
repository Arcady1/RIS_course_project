from flask import session, current_app

# Функция инициализирует пользователя
def get_session_group_name():
    user_type = session.get('group_name', 'unauthorized')
    session['group_name'] = user_type
    show_name = current_app.config['ACCESS_CONFIG'][f"{user_type}"]["name"]
    return show_name