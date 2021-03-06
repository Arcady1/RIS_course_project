# Стандартные пакеты
import os
from datetime import date

# Сторонние пакеты
from flask import Blueprint, render_template, request

# Модули проекта
from access.access import login_permission_required
from database.database import work_with_db
from database.sql_provider import SQLProvider
from utils.form_validator import is_form_valid

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

user_edit = Blueprint('user_edit', __name__, template_folder='templates')


# Отрисовка всех деталей и их удаление
@user_edit.route('/', methods=["GET", "POST"])
@login_permission_required
def edit_index():
    result = ''

    if request.method == "GET":
        sql = provider.get('get_all_details.sql')
        result = work_with_db(sql)

        if not result:
            result = 'Not found'
    elif request.method == "POST":
        item_id = request.form.get('item_id')

        # Проверка, была нажата кнопка "+" или "-"
        if request.form["action"] == "add":
            count = int(request.form.get('item_count')) + 1
        elif request.form["action"] == "remove":
            count = int(request.form.get('item_count')) - 1

        item_count = max(0, count)
        item_date = date.today().strftime("%Y-%m-%d")

        sql = provider.get('remove_detail.sql', detail_id=item_id, detail_count=item_count, detail_date=item_date)
        work_with_db(sql)

        sql = provider.get('get_all_details.sql')
        result = work_with_db(sql)

        if not result:
            result = 'Not found'
    return render_template('edit_index.html', result=result, col_titles=["ID", "Тип", "Материал", "Вес (г)",
                                                                         "Цена", "Кол-во на складе", "Обновление",
                                                                         " "])


# Страница добавления деталей
@user_edit.route('/insert', methods=["GET", "POST"])
@login_permission_required
def edit_insert():
    if request.method == "GET":
        return render_template('edit_insert.html', is_valid=[True] * 5, show_res=False)

    elif request.method == "POST":
        is_valid = []

        item_name = request.form.get('item_name')
        is_valid.append(is_form_valid(data=item_name, expected_data_type=str))

        item_material = request.form.get('item_material')
        is_valid.append(is_form_valid(data=item_material, expected_data_type=str))

        item_weight = request.form.get('item_weight')
        is_valid.append(is_form_valid(data=item_weight, expected_data_type=int, positive_num=True))

        item_price = request.form.get('item_price')
        is_valid.append(is_form_valid(data=item_price, expected_data_type=int, positive_num=True))

        item_count = request.form.get('item_count')
        is_valid.append(is_form_valid(data=item_count, expected_data_type=int, positive_num=True))

        # Проверка, все ли поля формы валидны
        if False in is_valid:
            valid_status = False
        else:
            valid_status = True

        item_date = date.today().strftime("%Y-%m-%d")

        # Если все данные - валидные
        if valid_status:
            sql = provider.get('add_detail.sql', detail_name=item_name, detail_material=item_material,
                               detail_weight=item_weight, detail_price=item_price, detail_count=item_count,
                               detail_date=item_date)
            work_with_db(sql)
        return render_template('edit_insert.html', is_valid=is_valid, valid_status=valid_status, show_res=True)
