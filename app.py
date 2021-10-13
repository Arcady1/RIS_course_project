from flask import Flask, render_template
from blueprint_query.blueprint_query import user_app

app = Flask(__name__)

app.register_blueprint(user_app, url_prefix='/user')

# Главное меню
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
