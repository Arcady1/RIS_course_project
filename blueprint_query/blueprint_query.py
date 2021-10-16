from flask import Blueprint, render_template, request, session
from database.database import work_with_db
from blueprint_query.sql_provider import SQLProvider
from RIS_course_project.access.access import login_permission_required
import json
import os

with open('database/config.json') as json_file:
    db_config = json.load(json_file)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
user_app = Blueprint('user_app', __name__, template_folder='templates')

# Страница вариантов запросов
@user_app.route('/queries')
@login_permission_required
def user_index():
    # group_permission_validation(json.load(open('configs/access.json')), session)
    return render_template('queries.html')

# Обработчик запроса 1 GET, POST
@user_app.route('/queries/query_1', methods=["GET", "POST"])
@login_permission_required
def query_1():
    result = ''

    if request.method == "POST":
        data = request.form.get('data')
        sql = provider.get('query_1.sql', city=data)
        result = work_with_db(db_config, sql)

        if not result:
            result = 'Not found'
    return render_template('query_1.html', result=result)

# Обработчик запроса 2 GET, POST
@user_app.route('/queries/query_2', methods=["GET", "POST"])
@login_permission_required
def query_2():
    result = ''

    if request.method == "POST":
        data = request.form.get('data')
        sql = provider.get('query_2.sql', weight=data)
        result = work_with_db(db_config, sql)

        if not result:
            result = 'Not found'
    return render_template('query_2.html', result=result)