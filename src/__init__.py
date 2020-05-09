from flask import Flask, redirect, url_for, render_template, request
from database import db
import config
from models import User

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        current_user = User.query.filter(User.username == username, User.password == password).first()
        if current_user :
            return redirect(url_for('get_users'))
        else:
            return '用户名或密码错误! 请确认后再登录!'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        repeat_password = request.form.get('repeat_password')
        if username == '' or password == '' or repeat_password == '':
            return '用户名和密码均不能为空！请重新输入！'
        elif password != repeat_password:
            return '两次密码不相等! 请核对后填写'
        else:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/delete', methods=['POST'])
def delete_user():
    user_id = int(request.form.get('id'))
    current_user = User.query.filter_by(id=user_id).first()
    db.session.delete(current_user)
    db.session.commit()
    return redirect(url_for('get_users'))


@app.route('/password', methods=['POST'])
def modify_password():
    user_id = request.form.get("id")
    new_password = request.form.get("new_password")
    current_user = User.query.filter_by(id=user_id).first()
    if new_password == '':
        return '新密码不能为空！'
    elif new_password == current_user.password:
        return '两次密码一致！'
    else:
        current_user.password = new_password
        db.session.commit()
        return redirect(url_for('get_users'))


@app.route('/add', methods=['POST'])
def add_user():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == '' or password == '':
        return '用户名或密码均不能为空！'
    else:
        new_user = User(username, password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('get_users'))


if __name__ == '__main__':
    app.run()