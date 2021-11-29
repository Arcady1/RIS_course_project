# Стандартные пакеты
import os

# Сторонние пакеты
from flask import Blueprint, render_template, session, request, current_app

# Модули проекта
from utils.session import get_session_group_name
from database.database import work_with_db
from database.sql_provider import SQLProvider

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

auth_app = Blueprint('auth_app', __name__, template_folder='templates')


# Функция возвращает group_name пользователя
def get_group_name_from_db(login, password):
    sql = provider.get('user_info.sql', user_name=login, user_password=password)
    result = work_with_db(sql)

    if not result:
        return None

    # Сохранение id пользователя, который вошел в систему
    session["user_id"] = result[0]["idusers"]

    return result[0]['user_group']


# Сценарий авторизации пользователя
@auth_app.route('/', methods=['GET', 'POST'])
def login_page():
    auth_result = ""

    if request.method == 'POST':
        login = request.form.get('login', None)
        password = request.form.get('password', None)
        group_name = get_group_name_from_db(login, password)
        config = current_app.config['ACCESS_CONFIG']

        if group_name in config.keys():
            session['group_name'] = group_name
            auth_result = "OK"
        else:
            auth_result = "NO"
    return render_template('auth.html', auth_result=auth_result, user_type=get_session_group_name())
