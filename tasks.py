from flask import Flask, request, session, redirect, url_for, render_template
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, or_
import datetime

# engine = create_engine('sqlite:///tasks.db', echo=True)
engine = create_engine("postgresql://xcnhbtjxnnbfuu:4f1961f672e831cf18722fb141ed5e304928a404cd2785ac0dc05bec11142f4d@ec2-34-255-134-200.eu-west-1.compute.amazonaws.com/d297cli1t1889p",echo = True)

meta = MetaData()

works = Table('works', meta,
    Column('id', Integer, primary_key = True),
    Column('worker', String),
    Column('fio', String),
    Column('date_start', String),
    Column('date_stop', String),
    Column('comment', String),
    Column('status', String),
    Column('done', String),
    Column('create', DateTime),
    Column('work', DateTime),
    Column('complete', DateTime),
              )

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
    Column('complete', DateTime),
    Column('done', String),
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
            session['login'] = request.form['username']
            return redirect(url_for('show'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return render_template('login.html')


def stat(task_status):
    conn = engine.connect()
    s = tasks.select().where(tasks.c.status == task_status)
    return len(conn.execute(s).fetchall())


def count():
    conn = engine.connect()
    s = tasks.select()
    return len(conn.execute(s).fetchall())


def count_works():
    conn = engine.connect()
    s = works.select()
    return len(conn.execute(s).fetchall())


def stat_works(task_status):
    conn = engine.connect()
    s = works.select().where(works.c.status == task_status)
    return len(conn.execute(s).fetchall())


@app.route('/show')
def show():
    if session.get('logged_in'):
        ids_new = stat('Новая')
        ids_new_works = stat_works('Новая')
        ids_work = stat('В работе')
        ids_work_works = stat_works('В работе')
        ids_complete = stat('Выполнена')
        ids_work_complete = stat_works('Выполнена')

        return render_template('show.html', ids_new = ids_new, ids_work = ids_work,
                               ids_complete = ids_complete, ids_new_works = ids_new_works,
                               ids_work_works=ids_work_works, ids_work_complete = ids_work_complete,
                               login = session['login']  )
    else:
        return render_template('login.html')


@app.route('/open')
def open():
    if session.get('logged_in'):
        conn = engine.connect()
        s = tasks.select().where(tasks.c.status == 'Новая')
        tasks_open = conn.execute(s)
        return render_template('open.html', tasks_open = tasks_open, login = session['login'] )
    else:
        return render_template('login.html')

@app.route('/work')
def work():
    if session.get('logged_in'):
        conn = engine.connect()
        s = tasks.select().where(tasks.c.status == 'В работе')
        tasks_work = conn.execute(s)
        return render_template('work.html', tasks_work = tasks_work, login = session['login'] )
    else:
        return render_template('login.html')

@app.route('/work_work')
def work_work():
    if session.get('logged_in'):
        conn = engine.connect()
        s = works.select().where(works.c.status == 'В работе')
        works_work = conn.execute(s)
        return render_template('work_work.html', works_work = works_work, login = session['login'] )
    else:
        return render_template('login.html')

# Архив задач
@app.route('/arhiv')
def arhiv():
    if session.get('logged_in'):
        conn = engine.connect()
        s = tasks.select().where(or_(tasks.c.status == 'Выполнена', tasks.c.status == 'Отменена'))
        tasks_arhiv = conn.execute(s)
        return render_template('arhiv.html', tasks_arhiv = tasks_arhiv, login = session['login'])
    else:
        return render_template('login.html')


# Архив переработок
@app.route('/work_arhiv')
def work_arhiv():
    if session.get('logged_in'):
        month_current = datetime.datetime.now().month
        conn = engine.connect()
        s = works.select().where(works.c.date_start[0] == '2', or_(works.c.status == 'Выполнена', works.c.status == 'Отменена'))
        works_arhiv = conn.execute(s)
        return render_template('work_arhiv.html', works_arhiv = works_arhiv, login = session['login'])
    else:
        return render_template('login.html')

@app.route('/new')
def new():
    if session.get('logged_in'):
        return render_template('new.html', login = session['login'])
    else:
        return render_template('login.html')

@app.route('/new_task', methods=['POST'])
def new_task():
    if session.get('logged_in'):
        ids = count()
        conn = engine.connect()
        conn.execute(tasks.insert().values(id = ids + 1, task = request.form['task_text'], status = 'Новая',
                                           fio = '', done ='', create = datetime.datetime.now()))
        return redirect(url_for('new'))
    else:
        return render_template('login.html')

@app.route('/new_work_task', methods=['POST'])
def new_work_task():
    if session.get('logged_in'):
        ids_works = count_works()
        date_start_t = request.form['date_start'].replace('T',' ')
        date_stop_t = request.form['date_stop'].replace('T',' ')
        conn = engine.connect()
        conn.execute(works.insert().values(id = ids_works + 1,  status = 'Новая',
                                           date_start = date_start_t,
                                           date_stop = date_stop_t, comment = request.form['comment'],
                                          worker = request.form['worker'], done ='', create = datetime.datetime.now()))
        return redirect(url_for('new_work'))
    else:
        return render_template('login.html')

@app.route('/open_work')
def open_work():
    if session.get('logged_in'):
        conn = engine.connect()
        s = works.select().where(works.c.status == 'Новая')
        open_work = conn.execute(s)
        return render_template('open_work.html', open_work = open_work, login = session['login'] )
    else:
        return render_template('login.html')

@app.route('/in_work', methods=['POST'])
def in_work():
    if session.get('logged_in'):
        conn = engine.connect()
        conn.execute(tasks.update().where(tasks.c.id == request.form['in_work']).
                     values(fio= session['login'], status= 'В работе' ,work=datetime.datetime.now() ) )
        return redirect(url_for('open'))
    else:
        return render_template('login.html')

@app.route('/in_work_work', methods=['POST'])
def in_work_work():
    if session.get('logged_in'):
        conn = engine.connect()
        conn.execute(works.update().where(works.c.id == request.form['in_work_work']).
                     values(fio=session['login'], status= 'В работе' ,work=datetime.datetime.now() ) )
        return redirect(url_for('open_work'))
    else:
        return render_template('login.html')

@app.route('/in_complete', methods=['POST'])
def in_complete():
    if session.get('logged_in'):
        conn = engine.connect()
        conn.execute(tasks.update().where(tasks.c.id == request.form['in_complete']).
                     values(status= 'Выполнена',complete=datetime.datetime.now() ) )
        return redirect(url_for('work'))
    else:
        return render_template('login.html')

@app.route('/in_work_complete', methods=['POST'])
def in_work_complete():
    if session.get('logged_in'):
        conn = engine.connect()
        conn.execute(works.update().where(works.c.id == request.form['in_work_complete']).
                     values(status= 'Выполнена',complete=datetime.datetime.now() ) )
        return redirect(url_for('work_work'))
    else:
        return render_template('login.html')

@app.route('/in_cancel', methods=['POST'])
def in_cancel():
    if session.get('logged_in'):
        conn = engine.connect()
        conn.execute(tasks.update().where(tasks.c.id == request.form['in_cancel']).
                     values(status= 'Отменена'), complete=datetime.datetime.now() )
        return redirect(url_for('work'))
    else:
        return render_template('login.html')

@app.route('/in_work_cancel', methods=['POST'])
def in_work_cancel():
    if session.get('logged_in'):
        conn = engine.connect()
        conn.execute(works.update().where(works.c.id == request.form['in_work_cancel']).
                     values(status= 'Отменена'), complete=datetime.datetime.now() )
        return redirect(url_for('work_work'))
    else:
        return render_template('login.html')

@app.route('/in_new', methods=['POST'])
def in_new():
    if session.get('logged_in'):
        conn = engine.connect()
        conn.execute(tasks.update().where(tasks.c.id == request.form['in_new']).
                     values(status= 'Новая'), complete=datetime.datetime.now() )
        return redirect(url_for('work'))
    else:
        return render_template('login.html')

@app.route('/in_work_new', methods=['POST'])
def in_work_new():
    if session.get('logged_in'):
        conn = engine.connect()
        conn.execute(works.update().where(works.c.id == request.form['in_work_new']).
                     values(status= 'Новая'), complete=datetime.datetime.now() )
        return redirect(url_for('work_work'))
    else:
        return render_template('login.html')


@app.route('/in_done', methods=['POST'])
def in_done():
    if session.get('logged_in'):
        conn = engine.connect()
        conn.execute(tasks.update().where(tasks.c.id == request.form['in_done']).
                     values(done= request.form['done_text']))
        return redirect(url_for('work'))
    else:
        return render_template('login.html')


@app.route('/in_work_done', methods=['POST'])
def in_work_done():
    if session.get('logged_in'):
        conn = engine.connect()
        conn.execute(works.update().where(works.c.id == request.form['in_work_done']).
                     values(done= request.form['done_text']))
        return redirect(url_for('work_work'))
    else:
        return render_template('login.html')

@app.route('/new_work')
def new_work():
    if session.get('logged_in'):
        conn = engine.connect()
        s = works.select().order_by(works.c.worker).distinct(works.c.worker).where(works.c.fio == session['login'])
        open_work = conn.execute(s)
        return render_template('new_work.html', open_work = open_work, login = session['login'])
    else:
        return render_template('login.html')

if __name__ == '__main__':
    app.run()