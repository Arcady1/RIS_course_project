from flask import Blueprint, render_template, session, request, current_app

# ====================================================================
from database.database import work_with_db
from blueprint_scenario_auth.sql_provider import SQLProvider
import os
import json

with open('database/config.json') as json_file:
    db_config = json.load(json_file)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
# ====================================================================

auth_app = Blueprint('auth_app', __name__, template_folder='templates')

# Функция возвращает group_name пользователя
def get_group_name_from_db(login, password):
    sql = provider.get('query_1.sql', user_name=login, user_password=password)
    result = work_with_db(db_config, sql)

    if not result:
        return None
    return result[0]['user_group']

# Сценарий авторизации пользователя
@auth_app.route('/', methods=['GET', 'POST'])
def login_page():
    auth_result = ''

    if request.method == 'POST':
        login = request.form.get('login', None)
        password = request.form.get('password', None)
        group_name = get_group_name_from_db(login, password)
        config = current_app.config['ACCESS_CONFIG']

        if group_name in config.keys():
            session['group_name'] = group_name
            auth_result = "Successful login!"
        else:
            auth_result = 'Invalid login or password!'
    return render_template('auth.html', auth_result=auth_result, user_type=session['group_name'])