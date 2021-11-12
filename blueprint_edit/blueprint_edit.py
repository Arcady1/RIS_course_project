from flask import Blueprint, render_template, request

# ====================================================================
from database.database import work_with_db
from blueprint_edit.sql_provider import SQLProvider
import os
import json

with open('database/config.json') as json_file:
    db_config = json.load(json_file)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
# ====================================================================

user_edit = Blueprint('user_edit', __name__, template_folder='templates')

# Отрисовка всех деталей и их удаление
@user_edit.route('/', methods=["GET", "POST"])
def edit_index():
    result = ''

    if request.method == "GET":
        sql = provider.get('get_all_details.sql')
        result = work_with_db(db_config, sql)

        if not result:
            result = 'Not found'
    elif request.method == "POST":
        item_id = request.form.get('item_id')
        sql = provider.get('remove_detail.sql', detail_id=item_id)
        work_with_db(db_config, sql)

        sql = provider.get('get_all_details.sql')
        result = work_with_db(db_config, sql)

        if not result:
            result = 'Not found'
    return render_template('edit_index.html', result=result, col_titles=["ID детали", "Тип", "Вес (г)",
                                                                         "Цена", " "])

# Страница добавления деталей
@user_edit.route('/insert', methods=["GET", "POST"])
def edit_insert():
    if request.method == "POST":
        item_name = request.form.get('item_name')
        item_weight = request.form.get('item_weight')
        item_price = request.form.get('item_price')
        sql = provider.get('add_detail.sql', detail_name=item_name, detail_weight=item_weight, detail_price=item_price)
        work_with_db(db_config, sql)
    return render_template('edit_insert.html')
