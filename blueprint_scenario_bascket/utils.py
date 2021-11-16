from flask import session

# Функция добавления товара в корзину
def add_to_basket(item):
    basket = session.get('basket', [])
    basket.append(item)
    session['basket'] = basket

# Функция очистки корзины
def clear_basket():
    if 'basket' in session:
        session.pop('basket')