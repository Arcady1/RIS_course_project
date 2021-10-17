from flask import Blueprint, render_template, session, request, current_app

auth_app = Blueprint('auth_app', __name__, template_folder='templates')

# Сценарий авторизации пользователя
@auth_app.route('/', methods=['GET', 'POST'])
def login_page():
    auth_result = ''

    if request.method == 'POST':
        login = request.form.get('login', None)
        password = request.form.get('password', None)
        config = current_app.config['ACCESS_CONFIG']

        if (str(login) in config.keys()) and (str(password) == config[login]['password']):
            session['group_name'] = login
            auth_result = "Successful login!"
        else:
            auth_result = 'Invalid login or password!'
    return render_template('auth.html', auth_result=auth_result, user_type=session['group_name'])