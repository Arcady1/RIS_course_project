# Стандартные пакеты
import os

# Сторонние пакеты
from flask import session

# Модули проекта
from database.database import work_with_db
from database.sql_provider import SQLProvider

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


# Функция добавления товара в корзину
def add_to_basket(product, customer_id):
    basket = session.get('basket', [])

    # Добавление id пользователя к каждому выбранному товару
    product["customer_id"] = customer_id
    # Ссылка на товар в корзине
    product_link = None

    # Проверка, есть ли товар уже в корзине
    for basket_el in basket:
        if basket_el["iddetail"] == product["iddetail"]:
            product_link = basket_el
            break;
    if product_link is None:
        # Добалвяем товар в сессию
        product["count"] = 1
        basket.append(product)
    else:
        product_link["count"] = product_link["count"] + 1

    # basket.append(product)
    session['basket'] = basket


# Функция очистки корзины
def clear_basket():
    if 'basket' in session:
        session.pop('basket')


# Функция добавления товара в коризу в БД
def add_to_BD(waybill_id, waybill_date):
    # Собранная корзина
    basket = session.get('basket', [])

    # Общая сумма заказа
    total_cost = 0

    for product in basket:
        total_cost += int(product["count"]) * int(product["detail_price"])

        # Внесение данных в waybill_str
        sql = provider.get('add_to_waybill_str.sql',
                           waybill_id=waybill_id,
                           details_count=product["count"],
                           detail_id=product["iddetail"])
        work_with_db(sql)

    # Внесение данных в waybill
    sql = provider.get('add_to_waybill.sql',
                       waybill_date=waybill_date,
                       waybill_id=waybill_id,
                       full_price=total_cost,
                       customer_id=session.get('customer_ID'))
    work_with_db(sql)

    # Функция очистки корзины в БД
    clear_basket()


def clear_basket_DB():
    sql = provider.get('clear_basket.sql')
    work_with_db(sql)
