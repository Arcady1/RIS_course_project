from flask import Blueprint, render_template

user_cart = Blueprint('user_cart', __name__, template_folder='templates')

@user_cart.route('/')
def cart_page():
    return render_template('cart.html')