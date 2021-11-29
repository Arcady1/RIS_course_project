# Стандартные пакеты
import json

# Сторонние пакеты
from flask import Flask, render_template, session
from flask_bootstrap import Bootstrap

# Модули проекта
from blueprint_query.blueprint_query import user_app
from blueprint_scenario_auth.scenario_auth import auth_app
from blueprint_scenario_bascket.routes import user_basket
from blueprint_edit.blueprint_edit import user_edit
from blueprint_waybills.blueprint_waybill import user_waybill
from utils.session import get_session_group_name

app = Flask(__name__)
app.register_blueprint(user_app, url_prefix='/user')
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(user_basket, url_prefix='/basket')
app.register_blueprint(user_edit, url_prefix='/edit')
app.register_blueprint(user_waybill, url_prefix='/all-waybills')

# Конфигурации Flask
app.config['SECRET_KEY'] = 'super secret key'
app.config['ACCESS_CONFIG'] = json.load(open('configs/access.json'))

# Подключение Bootstrap для стилизации сайта
Bootstrap(app)


# Endpoint - главное меню
@app.route('/')
def index():
    return render_template('index.html', user_type=get_session_group_name())


# Endpoint - выход из аккаунта
@app.route('/exit')
def index_exit():
    # Очистка сессии
    session.clear()
    return render_template('exit.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
