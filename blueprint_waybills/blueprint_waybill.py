# Стандартные пакеты
import os

# Сторонние пакеты
from flask import Blueprint, render_template, session, request, redirect, url_for

# Модули проекта
# TODO from access.access import login_permission_required
from .utils import get_details_info_from_waybill
from utils.session import get_session_group_name
from database.database import work_with_db
from database.sql_provider import SQLProvider

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

user_waybill = Blueprint('user_waybill', __name__, template_folder='templates')


# Отрисовка каталога товаров и корзины
@user_waybill.route('/', methods=["GET", "POST"])
def waybill_index():
    if request.method == "GET":
        sql = provider.get('get_all_customers.sql')
        result = work_with_db(sql)

        return render_template('all_customers.html',
                               user_type=get_session_group_name(),
                               result=result,
                               col_titles=["ID покупателя", "Договор заключён", "Имя", "Фамилия", "Город", ""])
    elif request.method == "POST":
        session["waybill_customer_id"] = request.form["user_id"]
        return redirect(url_for('user_waybill.customer_waybills', id=session.get('waybill_customer_id')))


@user_waybill.route('/<int:id>', methods=["GET", "POST"])
def customer_waybills(id=None):
    if id is None:
        return redirect(url_for('user_waybill.waybill_index'))
    sql = provider.get('get_customer_waybills.sql', customer_id=id)
    result = work_with_db(sql)

    # Подробная информация о каждом заказе клиента
    full_info_result = []

    for res in result:
        # Замена значения user_group на должность
        if res['user_group'] is not None:
            res['user_group'] = get_session_group_name(user_type=res['user_group'])

        # Получение подробностей о каждом заказе клиента
        full_info_result.append(get_details_info_from_waybill(res["idwaybill"]))

    print(result)
    print(full_info_result)
    return render_template('customer_waybills.html',
                           result=result,
                           full_info_result=full_info_result,
                           id=id,
                           col_titles=["ID накладной", "Дата формирования", "Полная стоимость", "Оформил", "Статус"],
                           col_sizes=["75", "210", "110", "100", "200"])
