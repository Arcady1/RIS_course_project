from flask import Blueprint, render_template, session, request
# import configs/access.json

auth_app = Blueprint('auth_app', __name__, template_folder='templates')

# Сценарий авторизации пользователя
@auth_app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('auth.html')
    elif request.method == 'POST':
        login = request.form.get('login', None)
        password = request.form.get('password', None)

        if login == 'l' and password == 'p':
            session['group_name'] = login
            return f"{session.keys()} {session.values()}"
        else:
            return 'Invalid login or password'