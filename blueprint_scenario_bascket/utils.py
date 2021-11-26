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
        # Если товар уже в корзине, то сохраняем ссылку на него
        if basket_el["iddetail"] == product["iddetail"]:
            product_link = basket_el
            break;
    # Еслм товара нет в корзине, то добавляем
    if product_link is None:
        # Добалвяем товар в сессию
        product["count"] = 1
        basket.append(product)
    else:
        # Добавление детали в корзину, но не больше, чем на складе
        product_link["count"] = min(product_link["count"] + 1, product_link["stock_count"])

    # basket.append(product)
    session['basket'] = basket


# Функция очистки корзины
def clear_basket():
    if 'basket' in session:
        session.pop('basket')

# Функция удаления выбранного пользователя из сессии
def clear_user_id():
    if 'customer_ID' in session:
        session.pop('customer_ID')


# Функция добавления товара в коризу в БД => нажата кнопка "Купить"
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

    # Очистка сессии
    clear_basket()
    clear_user_id()


def clear_basket_DB():
    sql = provider.get('clear_basket.sql')
    work_with_db(sql)
