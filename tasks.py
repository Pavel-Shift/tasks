from flask import Flask, request, session, redirect, url_for, render_template
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, select, func
import datetime

engine = create_engine('sqlite:///tasks.db', echo=True)
meta = MetaData()
users = Table('users', meta,
              Column('login', String, primary_key=True),
              Column('password', String),
              )

tasks = Table('tasks', meta,
    Column('id', Integer, primary_key = True),
    Column('task', String),
    Column('status', String),
    Column('fio', String),
    Column('create', DateTime),
    Column('work', DateTime),
    Column('comlete', DateTime),
)
app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='secret key 2021',
))

def auth(username_f, password_f):
    conn = engine.connect()
    s = users.select().where(users.c.login == username_f, users.c.password == password_f)
    result = len(conn.execute(s).fetchall())
    return result

@app.route('/')
def hello():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if auth(request.form['username'], request.form['password'])==0:
            error = 'Неверный пользователь или пароль'
        else:
            session['logged_in'] = True
            return redirect(url_for('show'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return render_template('login.html')

@app.route('/show')
def show():
    if session.get('logged_in'):
        return render_template('show.html')
    else:
        return render_template('login.html')

@app.route('/open')
def open():
    if session.get('logged_in'):
        return render_template('open.html')
    else:
        return render_template('login.html')

@app.route('/work')
def work():
    if session.get('logged_in'):
        return render_template('work.html')
    else:
        return render_template('login.html')

@app.route('/arhiv')
def arhiv():
    if session.get('logged_in'):
        return render_template('arhiv.html')
    else:
        return render_template('login.html')

@app.route('/new')
def new():
    if session.get('logged_in'):
        return render_template('new.html')
    else:
        return render_template('login.html')

@app.route('/new_task', methods=['POST'])
def new_task():
    if session.get('logged_in'):
        print(request.form['task_text'])
        conn = engine.connect()
        s = select([func.count()]).select_from(tasks)
        result = conn.execute(s)
        ids = result.fetchone()[0]
        print(ids)
        conn = engine.connect()
        conn.execute(tasks.insert().values(id = ids +1, task = request.form['task_text'], status = 'Новая',
                                           fio = '', create = datetime.datetime.now()))
        return render_template('show.html')
    else:
        return render_template('login.html')

if __name__ == '__main__':
    app.run()