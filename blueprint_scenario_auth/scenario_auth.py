from flask import Blueprint, render_template, session, request

auth_app = Blueprint('auth_app', __name__, template_folder='templates')

# Сценарий авторизации пользователя
@auth_app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('auth.html')
    elif request.method == 'POST':
        login = request.form.get('login', None)
        password = request.form.get('password', None)

        if login == 'login' and password == 'password':
            session['group_name'] = login
            return 'Success'
        else:
            return 'Invalid login or password'