from flask import Blueprint, render_template
from RIS_course_project.access.access import login_permission_required

user_cart = Blueprint('user_cart', __name__, template_folder='templates')

@user_cart.route('/')
@login_permission_required
def cart_page():
    return render_template('cart.html')