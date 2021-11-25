# Стандартные пакеты
import os

# Сторонние пакеты
from flask import session

# Модули проекта
from database.database import work_with_db
from database.sql_provider import SQLProvider

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


# Функция добавления товара в корзину
def add_to_basket(product):
    basket = session.get('basket', [])

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
def add_to_BD():
    basket = session.get('basket', [])

    for product in basket:
        sql = provider.get('add_product_to_basket.sql',
                           detail_id=product['idtest_details'],
                           detail_type=product['detail_type'],
                           detail_weight=product['detail_weight'],
                           detail_price=product['detail_price'])
        work_with_db(sql)


# Функция очистки корзины в БД
def clear_basket_DB():
    sql = provider.get('clear_basket.sql')
    work_with_db(sql)
