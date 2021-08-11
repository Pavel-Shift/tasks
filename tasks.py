from flask import Flask, render_template, Flask, request, session, g, redirect, url_for, abort, render_template, flash
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

engine = create_engine('sqlite:///tasks.db', echo=True)
meta = MetaData()
users = Table('users', meta,
              Column('login', String, primary_key=True),
              Column('password', String),
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
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            return redirect(url_for('show'))
    return render_template('login.html', error=error)

@app.route('/show')
def show():
    print(session.get('logged_in'))
    if session.get('logged_in'):
        return render_template('show.html')
    else:
        return render_template('login.html')

if __name__ == '__main__':
    app.run()