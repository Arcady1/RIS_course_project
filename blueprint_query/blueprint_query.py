# Стандартные пакеты
import os

# Сторонние пакеты
from flask import Blueprint, render_template, request

# Модули проекта
from access.access import login_permission_required
from utils.session import get_session_group_name
from utils.form_validator import is_form_valid
from database.database import work_with_db
from database.sql_provider import SQLProvider

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

user_app = Blueprint('user_app', __name__, template_folder='templates')


# Страница вариантов запросов
@user_app.route('/queries')
@login_permission_required
def user_index():
    return render_template('queries.html', user_type=get_session_group_name())


# Обработчик запроса 1 GET
@user_app.route('/queries/query_1')
@login_permission_required
def query_1():
    return render_template('query_1.html', is_valid=True)


# Результат запроса 1
@user_app.route('/queries/query_1/query_1_result', methods=["POST"])
@login_permission_required
def query_1_result():
    title = "Список покупателей из города"

    if request.method == "POST":
        data = request.form.get('data')

        # Валидация формы
        if is_form_valid(data=data, expected_data_type=str):
            sql = provider.get('query_1.sql', city=data)
            result = work_with_db(sql)
            title += f" {data if data else '-'}"

            if not result:
                result = 'Not found'
        else:
            return render_template('query_1.html', is_valid=False)

    return render_template('query_results.html', user_type=get_session_group_name(), title=title, result=result,
                           col_titles=["ID покупателя", "Дата заключения контракта", "Имя", "Фамилия", "Город"])


# Обработчик запроса 2 GET
@user_app.route('/queries/query_2')
@login_permission_required
def query_2():
    return render_template('query_2.html', is_valid=True)


# Результат запроса 2
@user_app.route('/queries/query_2', methods=["POST"])
@login_permission_required
def query_2_result():
    result = ''
    title = "Список деталей, больше"

    if request.method == "POST":
        data = request.form.get('data')

        # Валидация формы
        if is_form_valid(data=data, expected_data_type=int, positive_num=True):
            sql = provider.get('query_2.sql', weight=data)
            result = work_with_db(sql)
            title += f" {data if data else 0}г"

            if not result:
                result = 'Not found'
        else:
            return render_template('query_2.html', is_valid=False)
    return render_template('query_results.html', user_type=get_session_group_name(), title=title, result=result,
                           col_titles=["ID детали",
                                       "Название детали",
                                       "Материал",
                                       "Вес",
                                       "Стоимость",
                                       "Количество на складе",
                                       "Обновлено"])
