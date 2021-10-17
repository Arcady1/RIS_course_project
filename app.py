import requests
from flask import Flask, render_template, session, request
from blueprint_query.blueprint_query import user_app
from blueprint_scenario_auth.scenario_auth import auth_app
import json
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.register_blueprint(user_app, url_prefix='/user')
app.register_blueprint(auth_app, url_prefix='/auth')

# Используется для сессии
app.config['SECRET_KEY'] = 'super secret key'
app.config['ACCESS_CONFIG'] = json.load(open('configs/access.json'))

Bootstrap(app)

# Главное меню
@app.route('/', methods=["GET", "POST"])
def index():
    # Очистка сессии, если метод - POST
    if request.method == "POST":
        session.clear()
    return render_template('index.html', user_type=set_get_session_group_name())


def set_get_session_group_name():
    user_type = session.get('group_name', 'unauthorized')
    session['group_name'] = user_type
    return user_type

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
