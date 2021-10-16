from flask import Flask, render_template, session
from blueprint_query.blueprint_query import user_app
from blueprint_scenario_auth.scenario_auth import auth_app
# from RIS_course_project.access.access import login_required
import json

app = Flask(__name__)
app.register_blueprint(user_app, url_prefix='/user')
app.register_blueprint(auth_app, url_prefix='/auth')

# Используется для сессии
app.config['SECRET_KEY'] = 'super secret key'
app.config['ACCESS_CONFIG'] = json.load(open('configs/access.json'))

# Главное меню
@app.route('/')
def index():
    return render_template('index.html')

# Очистка сессии
@app.route('/session-clear')
def clear_session():
    session.clear()
    return ''

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
