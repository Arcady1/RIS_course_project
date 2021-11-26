# Стандартные пакеты
from datetime import date
import os

# Сторонние пакеты
from flask import Blueprint, render_template, session, request, redirect

# Модули проекта
from .utils import add_to_basket, clear_basket, add_to_BD, clear_user_id
from access.access import login_permission_required
from utils.session import get_session_group_name
from database.database import work_with_db
from database.sql_provider import SQLProvider

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

user_basket = Blueprint('user_basket', __name__, template_folder='templates')


# Отрисовка каталога товаров и корзины
@user_basket.route('/', methods=["GET", "POST"])
@user_basket.route('/<int:idcustomer>', methods=["GET", "POST"])
@login_permission_required
def register_orders_handler(idcustomer=None):
    # Инициализация ID выбранного пользователя и сохранение его в сессии
    session.get('customer_ID', None)

    # Если ID пользователя поменялся, то перезаписываем его
    if idcustomer:
        session['customer_ID'] = idcustomer
        # При смене покупателя происходит очистка корзины
        clear_basket_handler()

    # Если страница загрузилась, то отрисовываем её (список товаров и корзину)
    if request.method == "GET":
        current_basket = session.get('basket', [])
        sql = provider.get('basket_list.sql')
        items = work_with_db(sql)

        sql_customers = provider.get('customers_list.sql')
        customers = work_with_db(sql_customers)

        return render_template('basket_order_list.html',
                               items=items,
                               basket=current_basket,
                               customers=customers,
                               customer_id=session.get('customer_ID'),
                               user_type=get_session_group_name())
    # Если была нажата кнопка "Добавить товар в корзину"
    elif request.method == "POST":
        item_id = request.form['item_id']
        sql = provider.get('current_item.sql', item_id=item_id)
        item = work_with_db(sql)

        # Проверка, есть ли товар в БД
        if not item:
            return "Товар не найден"

        # Добавление товара в сессию
        add_to_basket(item[0], session.get('customer_ID'))
        return redirect('/basket')


# Функция описывает поведение при нажатии на кнопку "Купить"
@user_basket.route('/buy')
@login_permission_required
def buy_basket_handler():
    # Генерация ключа для waybill
    sql = provider.get('waybill_id_generator.sql')
    # Получение последнего id из waybil_str или 1, если таблица пустая
    res = work_with_db(sql)

    if res:
        waybill_id = res[0]["idwaybill_str"]
    else:
        waybill_id = 1

    # Время создания накладной
    waybill_date = date.today().strftime("%Y-%m-%d")

    # Добавление товаров в корзину в БД
    add_to_BD(waybill_id, waybill_date)

    clear_basket()
    clear_user_id()

    return render_template('order_is_processed.html')


# Функция описывает поведение при нажатии на кнопку "Очистить корзину"
@user_basket.route('/clear')
def clear_basket_handler():
    clear_basket()
    return redirect('/basket')
