from flask import Blueprint, render_template, session, request, redirect
from .utils import add_to_basket, clear_basket

# ====================================================================
from database.database import work_with_db
from blueprint_scenario_bascket.sql_provider import SQLProvider
import os
import json

with open('database/config.json') as json_file:
    db_config = json.load(json_file)

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
# ====================================================================

user_basket = Blueprint('user_basket', __name__, template_folder='templates')

# Отрисовка каталога товаров и корзины
@user_basket.route('/', methods=["GET", "POST"])
def register_orders_handler():
    if request.method == "GET":
        current_basket = session.get('basket', [])
        sql = provider.get('basket_list.sql')
        items = work_with_db(db_config, sql)

        return render_template('basket_order_list.html',
                               items=items,
                               basket=current_basket)
    elif request.method == "POST":
        item_id = request.form['item_id']
        sql = provider.get('current_item.sql', item_id=item_id)
        item = work_with_db(db_config, sql)

        if not item:
            return "Товар не найден"
        add_to_basket(item[0])

        return redirect('/basket')

# Функция описывает поведение при нажатии на кнопку "Купить"
@user_basket.route('/buy')
def buy_basket_handler():
    return redirect('/basket')

# Функция описывает поведение при нажатии на кнопку "Очистить корзину"
@user_basket.route('/clear')
def clear_basket_handler():
    clear_basket()
    return redirect('/basket')
