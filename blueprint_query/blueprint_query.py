from flask import Blueprint, render_template, request, session
from RIS_course_project.access.access import login_permission_required

# ====================================================================
from database.database import work_with_db
from blueprint_query.sql_provider import SQLProvider
import os
import json

with open('database/config.json') as json_file:
    db_config = json.load(json_file)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
# ====================================================================

user_app = Blueprint('user_app', __name__, template_folder='templates')


# Страница вариантов запросов
@user_app.route('/queries')
@login_permission_required
def user_index():
    return render_template('queries.html', user_type=session.get('group_name'))


# Обработчик запроса 1 GET
@user_app.route('/queries/query_1')
@login_permission_required
def query_1():
    return render_template('query_1.html', user_type=session.get('group_name'))


# Результат запроса 1
@user_app.route('/queries/query_1/query_1_result', methods=["POST"])
@login_permission_required
def query_1_result():
    result = ''
    title = "Список покупателей из указанного города"

    if request.method == "POST":
        data = request.form.get('data')
        sql = provider.get('query_1.sql', city=data)
        result = work_with_db(db_config, sql)

        if not result:
            result = 'Not found'
    return render_template('query_results.html', user_type=session.get('group_name'), title=title, result=result,
                           col_titles=["ID покупателя", "Дата заключения контракта", "Имя", "Город"])


# Обработчик запроса 2 GET
@user_app.route('/queries/query_2')
@login_permission_required
def query_2():
    return render_template('query_2.html')


# Результат запроса 2
@user_app.route('/queries/query_2', methods=["POST"])
@login_permission_required
def query_2_result():
    result = ''
    title = "Список деталей, больше указанного веса"

    if request.method == "POST":
        data = request.form.get('data')
        sql = provider.get('query_2.sql', weight=data)
        result = work_with_db(db_config, sql)

        if not result:
            result = 'Not found'
    return render_template('query_results.html', user_type=session.get('group_name'), title=title, result=result,
                           col_titles=["ID детали",
                                       "Название детали",
                                       "Материал",
                                       "Вес",
                                       "Стоимость",
                                       "Количество на складе",
                                       "Обновлено"])
